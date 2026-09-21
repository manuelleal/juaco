# PREREGISTRO — **BA-v** como candidato propio del nivel 5, con **ERR-90**: puertas ABSOLUTAS

**MISIÓN (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales, sin
retropropagación, que aprende, desaprende, generaliza, sobrevive y **se comunica con referencia**. Hoy, fase 5:
que el mensaje refiera a la **FAMILIA Y a la VARIANTE con la misma tabla** — `BAR-T ≤ 5/20` **Y** `PAR ≥ 15/20`
en las dos series, con un criterio que mida eso y no el nivel de otra celda.

**Fecha:** 2026-09-21. **Autor:** creador (Opus), por encargo del coordinador tras la decisión del director de
las 16:30 ("BA-v pasa a candidato aparte de la fase 5"). **Estado:** §0–§8 escritos **antes** del humo y de
cualquier serie. El §9 (humo) se añade después y **no toca** §0–§8. Lo que cambie después va en ERR numerado,
con fecha, motivo y semillas nuevas.

**Carpeta:** `experimentos/nivel05_familia_variante_BAv/` (nueva; no se toca `junta_fase5/A/`, `/B/`, `/BA/`,
`/C/`, `organismo/` ni nada congelado).

| | archivo | sha256(16) |
|---|---|---|
| constructor por anclas | `construye_familias_bav.py` | `944cafb8fc5687d8` |
| instrumento | `organismo_familias_bav.py` | `2dca0a3e239481f0` |
| arnés de identidad — **61/61** | `identidad_familias_bav.py` | `cf7655b379014a55` |
| runner (humo y serie) | `corre_familias_bav.py` | `4453754a9921e349` (en el humo: `0facf07b318d1bff`; ver §9.1) |
| diagnóstico de las muertes | `analiza_muertes_bav.py` → `DIAG_muertes.md` | — |
| tabla de las 4 series previas | `analiza_previas_bav.py` → `PREVIAS_4series.md` | — |
| **origen (sólo lectura)** | `experimentos/junta_fase5/BA/organismo_familias_ba.py` | `1f196ee786b2040d` |
| tronco (sólo lectura) | `organismo/organismo_v14.py` | `feefc88b1fd8d434` |

---

## 0. Qué hay medido, y por qué hace falta un criterio nuevo

`BA-v` = la ablación de BA en la que **la variante incompleta vota con lo que sabe** (`conj_tipo=2`). Es la
única fila de la fase 5 que ha cumplido **dos veces** el número crudo de la misión:

| celda | serie | CANAL | CORTADO | BAR-H | BAR-T | VALOR | dist(PAR) | dist(PAR0) | muertes | okU | MISIÓN |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BA-v | 921–940 | 16/19 | **0** | 4 | **2** | 4 | **18/19** | 0 | 46 | 0.667 | **SÍ** |
| BA-v | 941–960 | 18/19 | **0** | 7 | **4** | 2 | **17/19** | 1 | **104** | 0.667 | **SÍ** |
| A1 | 941–960 | 18/19 | 2 | 4 | 5 | 3 | 15/19 | 2 | 37 | 0.833 | SÍ |
| b5k3 | 941–960 | 17/19 | 1 | 12 | 6 | 3 | 11/19 | 1 | 50 | 0.667 | no |
| b6suf | 941–960 | 18/19 | 4 | 7 | 12 | 6 | 19/19 | 3 | 49 | 0.667 | no |

Y aun así cayó por la **letra relativa** del bloque 6: `R2 BAR-T ≤ CORTADO+3`, `R3 BAR-H ≤ CORTADO+5`,
`R4 VALOR ≤ CORTADO+3`. Con `CORTADO = 0` esas puertas se convierten en `≤ 3`, `≤ 5` y `≤ 3`, mientras A1 con
`CORTADO = 4` recibe `≤ 7`, `≤ 9` y `≤ 7`. **La letra premia tener una base alta**: bajar la base — que es lo
que queremos — endurece las tres puertas. No es una interpretación: es aritmética de la fórmula.

## 1. **ERR-90** (criterio nuevo; regla 11: toda enmienda que cambie la FORMA de un criterio lleva ERR)

> **ERR-90 (21-sep-2026, creador del nivel 5, por encargo del coordinador tras la decisión del director).**
> **Qué se observó:** las puertas R2, R3 y R4 del bloque 6 son relativas a `CORTADO` (`≤ CORTADO + 3/+5`), de
> modo que una celda que baja la base a 0 recibe umbrales más duros que una con base 4. En las series
> 921–940 y 941–960, `BA-v` (CORTADO 0/0) fue juzgada con `BAR-T ≤ 3` y `BAR-H ≤ 5` mientras `A1`
> (CORTADO 2–4) lo fue con `≤ 5–7` y `≤ 7–9`. **Causa:** criterio (la forma de la puerta, no un umbral).
> **Veredictos que toca: ninguno** — las series 821–860 y 921–960 **no se rejuzgan** (regla: no recalibrar tras
> ver datos); quedan como están, con su letra. **Corrección:** para `BA-v`, y sólo en semillas NUEVAS, las
> puertas pasan a ser **ABSOLUTAS** (P0–P7 de §3), la misión (`BAR-T ≤ 5` Y `PAR ≥ 15`) no se toca, y R6 se
> juzga con la base `b4b` corrida en la misma serie e impresa por el runner (ERR-89). **Regla derivada:** una
> puerta de especificidad no se normaliza por la tasa base de la propia celda cuando bajar esa tasa es parte
> de lo que se está midiendo; se equilibra con la puerta del lado contrario (aquí `CANAL ≥ 15`).

**Por qué lo absoluto no es una puerta más floja.** El par `CANAL ≥ 15` + `BAR-T/VALOR/CORTADO ≤ 5` es una
medida **balanceada** (trampa 2): un organismo que no come nunca falla P1, y uno que come siempre falla P3/P4.
Entre los dos no queda hueco para pasar sin discriminar. La normalización por `CORTADO` sobraba, y además
hacía que la puerta dependiera de un brazo distinto del que juzga.

## 2. Hipótesis y mecanismo (memoria nueva: **CERO** en el candidato)

> **Dentro del tipo VARIANTE, el voto gana a la abstención: una casilla de variante que no consta no debe
> hacer callar ni al tipo ni a la tabla, y la conjunción de la FORMA basta para fijar la familia.** Es lo que
> BA declaró antes de los datos ("si `BA-v` cumple la misión y `BA` no, el resultado es `BA-v`"), y se cumplió.

El candidato es `conj_tipo=2` sobre el instrumento ya construido: **ni un array, ni un contador, ni un bit
nuevo**. Lo único que se añade al instrumento es un **control** (`baraja_msg`), apagado en todas las celdas
menos en la suya.

**El control nuevo, `baraja_msg=1` (celda `BA-v-sh`): la MEMORIA BARAJADA.** El mensaje escribe **la misma R**
en una **casilla permutada** de la misma celda: misma cantidad de información, misma trayectoria hasta el paso
de la entrega (la permutación sale de un `Generator` propio y **no consume el azar del organismo**; el arnés lo
comprueba comparando `canal_t_msg`, `canal_t_entrega`, `canal_gan_pre`, `canal_bin` y `canal_gan_k_pre`), y
**correspondencia destruida**. Es la baraja de N1/N3d llevada a la tabla.

## 3. LAS PUERTAS (todas ABSOLUTAS), con el número justificado en las CUATRO series previas

Base: `PREVIAS_4series.md` (821–840 y 841–860 de la junta; 921–940 y 941–960 de BA). **Ningún umbral sale del
valor que sacó `BA-v`**; cada uno sale de un control o del enunciado de la misión.

| puerta | letra | de dónde sale el número | valores medidos (4 series) |
|---|---|---|---|
| **P0** montaje | `N ≥ 18` semillas válidas por celda | P-I2 del bloque 6 (emisor ≥ 18/20); con N < 18 no se lee nada | N = 18–19 |
| **P1** CANAL | `≥ 15` | R1 del bloque 6, sin cambio; es el **lado contrario** que equilibra P2–P5 | 16, 17, 18 en las 16 filas |
| **P2** CORTADO | `≤ 5` | R1 del bloque 6, sin cambio; deja de usarse como base de nada | 0–6 (sólo `b6suf` 6 una vez) |
| **P3** BAR-T | `≤ 5` | **el número de la misión** que fijó el director | b5k3 2–7 · A1 5–9 · BA 4–5 · **b6suf 8–12** |
| **P4** VALOR | `≤ 5` | el mismo número: un mensaje vacío no puede licenciar más comida que uno sobre otro token | 1–8 (A1 6–7, BA 6–8) |
| **P5** BAR-H | `≤ 10` | **el peor lector de variante ya medido**: `b6suf` 10 y `A1` 10 en 821–840. El lector que por construcción no separa a la hermana (`b5k3`) da 12–13 en las cuatro series | b5k3 12,13,12,12 · b6suf 4–10 · A1 4–10 · **BA 14,15** |
| **P6** PAR | `dist ≥ 15` **y** `dist(PAR0) ≤ 5` | `15` es el número de la misión; `PAR0 ≤ 5` sustituye "≥ gemelo+5" por el mismo umbral absoluto de los brazos mudos | dist 7–19 · PAR0 0–7 |
| **P7** R6 (coste) | `muertes ≤ 1.5 × muertes(b4b)` **Y** `okU ≥ okU(b4b) − 0.10`, con `muertes` = **mediana sobre semillas de `deaths` del brazo CANAL** y `okU` = mediana de `B4.okU` del brazo CANAL, **de la misma serie** | la letra exacta del §7.6 del preregistro de BA, sin tocar; la base `b4b` (k1v0) va en `--celdas` y el runner imprime la puerta (**ERR-89**) | nunca medida |
| **MISIÓN** | `BAR-T ≤ 5` **Y** `dist(PAR) ≥ 15` | del director, intacta | BA-v 2/18 y 4/17 |

**Se declara candidato sólo si pasa P0–P7 y la MISIÓN en LAS DOS series** (961–980 y 981–1000). Cualquier
puerta que caiga en cualquiera de las dos cierra la línea; no hay lectura de subconjunto preparada.

**Dos avisos de instrumento que escribo ANTES de correr, y que no cambian la letra:**
1. **La mediana de `deaths` es un estadístico de filo** (`DIAG_muertes.md` §1): la distribución es bimodal
   (régimen normal 15–180, régimen de hambre 200–1331, con un hueco vacío entre ~180 y ~450 en las 10
   combinaciones serie × celda). Con 5–7 de 19 semillas en el régimen de hambre, la mediana se sienta en la
   posición 10 de 19 y **una sola semilla la mueve de 46 a 104**. La puerta sigue siendo la mediana (letra
   exacta); junto a ella el runner imprime, **como diagnóstico que nunca la anula**, cuántas semillas mueren
   más de 1.5× su propia base pareada y cuántas están en régimen de hambre.
2. **`okU` está cuantizada en pasos de 1/6 = 0.1667** (`n_U = 6`), así que la tolerancia de 0.10 es **menor que
   la resolución de la medida**: en la práctica R6b exige `okU(BA-v) ≥ okU(b4b)`. Lo dejo escrito porque es la
   forma más probable de que el candidato muera, y no quiero que parezca un descubrimiento posterior.

## 4. Brazos, celdas, emisor y semillas

- **Brazos:** los **7 del bloque 6**, dirección (−) sola (ERR-53), sin añadir ni quitar: `CANAL`, `CORTADO`
  (gemelo mudo), `BAR-H`, `BAR-T`, `VALOR`, `PAR`, `PAR0`. Todo `com`/`dist` por **conducta de la boca** (ERR-44).
- **Celdas (6):** `b4b` (**base de R6, obligatoria**; el runner la añade si falta), `b5k3` y `b6suf` (líneas
  base de instrumento), `A1` (el control que más importa), **`BA-v`** (el candidato) y **`BA-v-sh`** (el
  control de memoria barajada).
- **Emisor:** el del bloque 6 **sin tocar** (b4b bit a bit). Se mide **la lectura, no el habla**.
- **Semillas NUEVAS: `961–980`, réplica `981–1000`.** T = 100 000. Ninguna se ha usado: 821–900 fueron de la
  junta y de C, 901–903 y 911 de humos, 921–960 de las dos series de BA. **Humo: semilla 912** (el runner
  rechaza cualquier semilla de 821–1000).
- **Puertas de montaje heredadas, sin cambio:** P-I1 identidad 100 %; **P-I2** emisor ≥ 18/20 (las semillas sin
  mensaje se excluyen y se reportan); P-I3 prefijo exacto contra el gemelo de la misma celda; P-I4 exclusión
  por semilla (ERR-70); **P-I5** `fam1 = 1` se reporta por brazo y la semilla vacua sale del numerador **y** del
  denominador de todos los brazos de esa celda, con el mismo trato para la línea base.

## 5. PREDICCIÓN NUMÉRICA, FIRMADA (mediana y rango, en **cada** una de las dos series)

| puerta | predicción (rango) | probabilidad de pasar **las dos** series |
|---|---|---|
| P0 N ≥ 18 | 19 (18–20) | 90 % |
| P1 CANAL ≥ 15 | **17 (15–19)** | 80 % |
| P2 CORTADO ≤ 5 | **1 (0–3)** | 92 % |
| P3 BAR-T ≤ 5 | **3 (1–6)** | 65 % |
| P4 VALOR ≤ 5 | **3 (0–6)** | 70 % |
| P5 BAR-H ≤ 10 | **6 (3–10)** | 75 % |
| P6 dist ≥ 15 y PAR0 ≤ 5 | **dist 16 (13–19)**, PAR0 1 (0–4) | 60 % |
| **P7 R6 muertes ≤ 1.5×** | razón **1.4× (0.8–2.6×)** | **45 %** |
| **P7 R6 okU** | `okU(BA-v)` 0.667 (0.583–0.833); `okU(b4b)` 0.667 (0.667–0.833) | **55 %** |
| MISIÓN | BAR-T 3, dist 16 | 55 % |
| **TODO (candidato declarado)** | — | **20 %** |

**Contrastes pareados que firmo aparte** (no dependen del nivel absoluto):
1. `CANAL(BA-v) − BAR-T(BA-v) ≥ 10` en las dos series (medido 14 y 14; `b5k3` 9–15, `b6suf` 4–8).
2. `CANAL(BA-v) − BAR-H(BA-v) ≥ 8` en las dos (medido 12 y 11; `b5k3`, que no puede separar a la hermana, 4–5).
3. **`CANAL(BA-v-sh) ≤ CORTADO(BA-v-sh) + 3`**: con la tabla barajada el mensaje deja de licenciar la mordida.
4. `CORTADO(BA-v) ≤ CORTADO(A1)` en las dos (medido 0 contra 4 y 2).

**Lo que espero del mecanismo** (`canal_lee_ref` en el paso de la entrega, para el referente): en `CANAL`
valor > 0 con 3/3 de FORMA; en `BAR-T` y `VALOR` valor ≤ −3 con 3/3 de FORMA; en **`BA-v-sh` la tabla NO habla
para el referente** (`habla = False` o 0/3 exactas de FORMA), porque la R del mensaje cayó en otra casilla.

## 6. Controles que pueden fallar (y lo digo antes)

- **`BA-v-sh` ≈ `BA-v` en CANAL.** Si con la memoria barajada el receptor sigue comiendo igual, no está
  leyendo el mensaje: está comiendo porque llegó un mensaje, y **todo lo demás da igual** — el candidato muere
  aunque pase las siete puertas. Es el control más fuerte de este preregistro y el que más me puede doler.
- **R6.** El candidato habla más que A1, así que debería morir menos, no más. Si muere más de 1.5× `b4b`,
  la puerta de seguridad lo mata, como mató a k = 5. **Le doy menos del 50 %** (ver §5) y no voy a discutir
  la mediana si cae.
- **`b5k3` y `b6suf` tienen que reproducir sus números de las cuatro series dentro de ±4.** Si no, el
  instrumento o el montaje cambiaron y **no se lee ningún veredicto** (regla 14, ERR-38).
- **`CORTADO(BA-v) > 5`.** Entonces la base de BA-v no era 0 y el motivo entero de ERR-90 se evapora: habría
  que juzgarlo con la letra relativa, y esa ya se sabe que cae.
- **`BA-v` ≡ `A1`.** Si las dos filas salen idénticas hasta el último decimal, una vía está apagada y se
  revisa el instrumento antes de leer nada (ERR-38).

## 7. Qué me refuta (declarado ahora)

1. **`BAR-T > 5` o `dist(PAR) < 15`** en cualquiera de las dos series nuevas → los dos aciertos de 921–960
   eran de las semillas; la línea BA/BA-v se cierra.
2. **`CANAL(BA-v-sh) > CORTADO(BA-v-sh) + 3`** → la lectura no es referencial; se cierra la línea entera y se
   revisa hacia atrás qué medían BA y A1.
3. **P7 (R6) cae en las dos series** → el candidato muere por coste, y la frase que queda es "lee mejor y vive
   peor".
4. **`CANAL < 15`** → la conjunción de forma es demasiado exigente y mata el canal (se mira `fam1`/P-I5 y
   `canal_lee_ref` antes de culpar al mecanismo).
5. **Todo baja a la vez, `CANAL` incluido** → no hay referencia: hay un organismo que dejó de leer la tabla.
   Lo distinguen `CORTADO`, `BA-v-sh` y las celdas `b5k3`/`b6suf` de la misma serie.

Nada de esto se recalibra después de ver datos. Un cambio de umbral, brazo, mecanismo o criterio exige
preregistro nuevo, semillas nuevas y ERR numerado.

## 8. Las cuatro trampas, revisadas (regla 5 de EQUIPO.md)

1. **Canal simétrico.** No lo es y se comprueba: el emisor es `b4b` bit a bit y **no cambia** entre celdas; el
   receptor no ve al emisor (el mensaje entra como `(t, ref, P, R)`); `CORTADO` y `PAR0` son los gemelos mudos;
   `BAR-H`/`BAR-T`/`VALOR` prueban que el **contenido** del campo de referencia importa; y **`BA-v-sh` prueba
   que importa la DIRECCIÓN en que ese contenido se escribe**, con la misma cantidad de información y la misma
   trayectoria previa. El arnés incluye `CANAL ≠ CORTADO`, `HERMANA ≠ CANAL`, `OTRO TOKEN ≠ CANAL` y
   `BARAJADA ≠ CANAL` como controles que DEBEN diferir (61/61).
2. **Acierto sin balancear.** No hay "acierto": la medida es binaria y **pareada** — mordió o no en su primera
   exposición de la vida al referente — y las puertas van **en los dos sentidos** (P1 obliga a comer cuando el
   mensaje dice comida; P2–P5 obligan a no comer cuando no lo dice). Ésa es la razón por la que quitar la
   normalización por `CORTADO` no afloja el criterio (§1).
3. **Mundo que se come la comida.** El mundo es el de familias del bloque 1/2, **importado y no recopiado**,
   con `renov=1.0` y deriva; el muestreo no lo fija el candidato. El coste es puerta (P7) y ahora además se
   **diagnostica**: mordidas totales, de comida y de veneno, `frac_veneno` por cuartil y `frac_regalo` (la
   fracción del gasto que el organismo cubre resucitando).
4. **Sitios fijos que se memorizan.** P-I4 exige que la **primera exposición de la vida** al referente sea la
   de después de la entrega (y excluye la semilla si no); los patrones se regeneran con `fam_seed` por semilla;
   el candidato no añade ningún sitio ni índice fijo (la dirección la calcula `_dir_var` de la retina presente),
   y la permutación del control se recalcula por semilla.

---

## 9. HUMO — resultado (§0–§8 NO se tocaron)

### 9.0 Identidad: **61/61** (`identidad_bav_salida.txt`, un proceso, semillas 1–3, 535 s)
Apagado (`baraja_msg=0`) ≡ `organismo_familias_ba` BIT A BIT en 16 casos (8 mundos × (k, sufijo)) **y con las
seis configuraciones de lectura encendidas, incluida `conj_tipo=2` (el candidato)**, con el canal en sus tres
modos y a T = 120 000 sin consumir rng; cadena ≡ a1 ≡ b6 ≡ b5 ≡ b4b ≡ `organismo_familias` ≡ **`organismo_v14`
(TRONCO)** ≡ `v15f_on`; inercia del control (sin canal, con canal mudo y sin tabla); **el prefijo hasta la
entrega es idéntico con y sin baraja** (`canal_t_msg`, `canal_t_entrega`, `canal_gan_pre`, `canal_bin`,
`canal_gan_k_pre`): el control no toca el azar del organismo; `baraja_perm` son 66 permutaciones completas y
mueven la casilla en 61–62 de las 66 celdas; la regla de BA-v reimplementada FUERA coincide con `W_tabla` en
los 32 estímulos y `habla(A1) ⊆ habla(BA-v) ⊆ habla(A1-d)` (A1 habla 16/32, BA-v 32/32, el tipo VARIANTE está
incompleto en 16/32 — el mismo dato que halló el arnés de BA); 8 perillas mal escritas que lanzan; **7
controles que DEBEN diferir**, todos 2/2 o 3/3, incluido el nuevo `BA-v con memoria barajada ≠ BA-v`.

### 9.1 Coste declarado (regla 3)
UN proceso, sin `Pool`. **1 semilla (912) × (1 emisor + 5 receptores) = 6 corridas de 100 000 pasos**, 54.5 s
de pared. El runner **se para** si el plan se pasa. Semilla 912: de la banda de humos (901–920), fuera de
821–900 y de 921–1000. Había 2 procesos python ajenos vivos (de otro repo) y **no se tocaron**.

**Cambio del runner DESPUÉS del humo, declarado:** una sola línea, dentro de `serie()` y sólo de LOG — P-I5 pasa a reportarse en **las seis celdas** en vez de sólo en la última (que con el orden nuevo era el control barajado). No toca `humo()`, ni `corre()`, ni `tabla()`, ni ninguna puerta, ni el organismo. sha del runner en el humo `0facf07b318d1bff`; sha entregado `4453754a9921e349`. El humo NO se repite: gastaría 6 corridas más del presupuesto por una línea de log.

### 9.2 Los números (`datos/humo/humo_bav_20260921_144432.log` / `.json`, crudo `5ad5c4b06fd86b94`)

Montaje: emisor 1/1 (`T1v2`, R = +1.0, t = 10 187, tras 1 exposición); **regla 14: 33 campos comunes,
IDÉNTICOS campo a campo con la entrada del bloque 6**; entrega en t = 66 677 (66 814 en `b4b`); la boca leyó
la vía **LENTA** en las 5 corridas (P-I5 limpio); `abstiene` 0/32 en las cinco. **Las ocho líneas de puerta
(P0–P7) y la MISIÓN se imprimen para las tres celdas, con `n/d` donde el brazo no se corrió** — que es lo que
pedía la regla derivada de ERR-89.

| celda · brazo | `LEE(ref)` = [valor, habla, FORMA, VARIANTE] | comió | muertes | mord. comida | `frac_regalo` |
|---|---|---|---|---|---|
| `b4b` · CANAL | — (un solo tipo) | **1** | 33 | 6 099 | 0.025 |
| `BA-v` · CANAL | **+3.0, True, 3/3, 3/3** | **1** | 511 | 1 962 | 0.383 |
| `BA-v` · CORTADO (mudo) | −6.0, True, 3/3, 2/3 | 0 | 490 | 2 022 | 0.368 |
| **`BA-v-sh`** · CANAL (barajada) | **−5.0, True, 3/3, 3/3** | **0** | 491 | 2 030 | 0.368 |
| `BA-v-sh` · CORTADO | −6.0, True, 3/3, 2/3 | 0 | 490 | 2 022 | 0.368 |

**R6 se imprime y tiene base:** `BA-v` 511 / `b4b` 33 = **15.5×** en esta semilla (CAE), okU +0.167 (pasa).
Con n = 1 eso **no dice nada** sobre la puerta; lo que sí dice es que la línea existe y que la base está.

### 9.3 PREDICCIÓN PROPIA REFUTADA (la declaro yo, antes de la serie)

Escribí en §5: *"en `BA-v-sh` la tabla **NO habla** para el referente (`habla = False` o 0/3 exactas de
FORMA)"*. **Es falso:** con la tabla barajada la tabla **habla igual** (True, 3/3 y 3/3) — y aun así el
receptor **no come**. El mecanismo dice por qué, y es exactamente la lección que B ya había escrito: para el
paso t = 66 677 la experiencia propia del receptor ya ha visitado esas casillas, así que la dirección
"consta"; lo que el mensaje barajado no hace es **poner su +R en la casilla del referente**, y entonces la
tabla contesta con el valor propio del receptor, que es **negativo** (−5.0, prácticamente el −6.0 del gemelo
mudo). **El control funciona mejor de lo que yo lo había descrito**: no apaga la tabla, sólo le quita la
correspondencia, que es justo lo que había que barajar. La predicción de §5 queda refutada por mí y la
sustituye —para la serie— el contraste 3 de §5, que sí firmé y que no cambia:
`CANAL(BA-v-sh) ≤ CORTADO(BA-v-sh) + 3`.

### 9.4 Lectura de R6 en su contexto, escrita ANTES de la serie (no cambia ni una letra)

La base de R6 es `b4b`: **k = 1, un solo tipo, lectura disyuntiva** — el lector más permisivo de toda la
cadena. En el humo come 3× más que el candidato (6 099 contra 1 962 mordidas de comida) y cubre con el
"regalo" de resucitar el 2.5 % de su gasto contra el 38 % del candidato. Predicción que añado aquí, y que la
serie contesta sola porque el runner imprime R6 **para las seis celdas**: es muy posible que **ninguna** celda
de k = 3 pase R6 contra `b4b` — ni `b5k3` ni `b6suf`, que son bloques ya registrados. Si eso pasa, la letra de
R6 se aplica igual al candidato (no se recalibra nada), pero el registro tendrá que decir que **R6 contra
`b4b` no separa al candidato: separa k = 1 de k = 3**, y el criterio del nivel 5 necesitará una base de coste
que sea del mismo orden (p. ej. `b5k3`) en su próximo preregistro, con su ERR y sus semillas.

**El mecanismo del coste, que los crudos de BA no podían medir y este runner sí:** las mordidas totales, de
comida y de veneno y `frac_regalo` entran ahora en cada fila. En la semilla 912 el candidato **no se envenena
más** (19 contra 118 mordidas de veneno de `b4b`): **come menos**. Si eso se repite en la serie, las 104
muertes de 941–960 son **abstinencia**, no imprudencia — la misma pesimista `min(forma, variante)` que le da
`CORTADO 0` le quita comida. Con n = 1 es una hipótesis, no un resultado.

---

## 10. EL COMANDO DE LA CONFIRMACIÓN (lo corre el coordinador; reglas 3 y 11)

```bat
cd C:\Users\User\Documents\PROYECTOS\JUACO\bundle
python -u experimentos/nivel05_familia_variante_BAv/corre_familias_bav.py --serie --desde 961 --pool 6
python -u experimentos/nivel05_familia_variante_BAv/corre_familias_bav.py --serie --desde 981 --pool 6
```

- Celdas por defecto: `b4b,b5k3,b6suf,A1,BA-v,BA-v-sh` (6). `b4b` no se puede quitar: si no está, el runner la
  añade y lo escribe en el log (**ERR-89**).
- **Coste por serie:** 20 emisores + 6 celdas × 7 brazos × ~19 semillas = **818** corridas de 100 000 pasos
  (la serie de BA fueron 665 en 1 149–1 299 s con Pool 8; con Pool 6 esperar **~25–35 min por serie**).
- `--pool N` manda sobre `JUACO_POOL` (ERR-86; en PowerShell la variable de entorno no pasa al hijo).
- Escribe `serie_bav_s961-980_*_crudo.json` **antes** de cualquier análisis (ERR-54), el log desde el arranque
  (regla 10) con una línea cada 40 corridas, la comprobación **campo a campo** de la regla 14, P-I5 por brazo y
  la tabla con **las ocho líneas de puerta (P0–P7) y la MISIÓN por celda**, más la letra relativa del bloque 6
  marcada como referencia histórica que **no decide**.
- La serie **se para sola** antes de gastar una corrida si un sha de origen cambió o si la entrada difiere del
  bloque 6 en algo que no sea una perilla de celda.
