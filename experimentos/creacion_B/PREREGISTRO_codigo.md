# PREREGISTRO — B-5 **DESAMBIGUAR CÓDIGOS**: división por ausencia de consecuencia bajo retina distinta (nivel 4)

CREADOR B, 18-sep-2026, 08:55. Escrito **antes de cualquier serie** y antes del humo (§8 se añade después y no toca
§1–§7). Lo corre el coordinador (`corre_codigo.py`, subprocesos secuenciales: nunca dos `Pool`). Sin `Pool` por mi
parte, sin commits. Misión: llegar a la AGI por este camino; el método manda sobre el cómo.

## 1. El hecho (medido, registro 08:16) y su tamaño real (medido aquí, sin simular)

**Alias de código.** Con `K = 3` celdas de 90, dos estímulos distintos reciben el MISMO código de Kenyon. En el mundo
vivo (4 estímulos), la sal —que no informa (`R = 0`)— hereda el valor del veneno cuando comparten código
(`|W[sal]|` 1.45 contra 0.0 en semillas limpias), el veneno pierde la mitad del miedo (−1.45 contra −3.0), la
evitación multiplica ×7 las exposiciones, no hay divisiones, persiste sin sed (S-5) y la puerta por código no lo
repara (S-6). Es una propiedad estructural del código del tronco v9–v14.1.

**Negativo estructural** (`negativo_codigo.py`, semillas 1–200, `negativo_codigo_s1-200.json` 29df6ce017eb7389;
construye `KW` como `organismo_v14.run` y lee los códigos; 0.1 s; copia verificada contra `diagnostico_codigos.py`):

| mundo | par (px compartidos) | mismo código (3/3) | 2 de 3 | 1 de 3 | 0 |
|---|---|---|---|---|---|
| tronco/vivo, 4 patrones, con `cond()` | A–B (1) | 0 % (prohibido por `cond()`) | 0 % | 0 % | 100 % |
| | A–C (1) | 0 % | 7.0 % | 37 % | 56 % |
| | A–D (0) | 0 % | 0 % | 10.5 % | 89.5 % |
| | B–C (1) | **1.0 %** | 7.5 % | 36.5 % | 55 % |
| | **B–D (2)** | **5.0 %** | **27.0 %** | 53 % | 15 % |
| | **C–D (2)** | **4.0 %** | **28.5 %** | 50.5 % | 17 % |
| | **algún par con el mismo código** | **18/200 = 9.0 %** | ≥ 2/3 en algún par: 128/200 = 64 % | | |
| regla (`bateria_generaliza`), 20 patrones, sin `cond()` | por par (190 pares/semilla) | **1.52 %** | 17.9 % | | |
| | pares idénticos por semilla | mediana **2** [0, 19]; **170/200 semillas** con alguno | 2/3: mediana 31.5 [12, 110] | | |
| | **fuga px0**: test con el código exacto de un train | **135/200 semillas** (mediana 1, máx. 11); 291 fugas, 176 de la misma valencia, **115 de valencia opuesta** | | | |

Lectura: el alias no es raro; es **la regla** en cuanto hay más de dos estímulos. Con dos (v14) `cond()` lo prohíbe y
por eso nunca se vio. En el mundo de regla el 85 % de las semillas tienen al menos un par de patrones con el mismo
código, y en 2 de cada 3 semillas un patrón nunca visto lee **exactamente** la celda de uno entrenado (40 % de esas
veces con la valencia contraria): parte de lo que `bateria_generaliza` mide como generalización o como fallo es alias.

## 2. Hipótesis

**H-B5.** El organismo no separa la sal del veneno porque su único órgano separador —la división por conflicto de
signo (v11)— exige `Wb[c]·R < 0` y la ausencia de consecuencia (`R = 0`) no tiene signo. Si la celda consolidada
lee "bajo una retina distinta no pasó nada" como **desconfirmación** y divide, la hija (ciega fuera del patrón nuevo,
nacida sin valor) se lleva el código del estímulo mudo, el veneno conserva su celda y su miedo, y la evitación
desaparece porque ya no hay valor prestado que evitar.

## 3. Mecanismo mínimo (local; memoria nueva cero; constantes nuevas cero; rng intacto)

Una condición y una rama en la línea de división de v11, dentro de la celda que divide:

```
v14.1:  divide si   Wb[c]*R < 0                 y |Wb[c]| > 0.2  y  kj@P > KW[c]@P  y hay celda libre
B-5:    divide si  (Wb[c]*R < 0  o  R == 0)     y |Wb[c]| > 0.2  y  kj@P > KW[c]@P  y hay celda libre
fisión: R > 0 → como v11;  R < 0 → como v11;  R == 0 → Wp[j] = Wn[j] = 0 (la hija nace SIN valor), la madre conserva el suyo
```

`kj = clip(0.95·KW[c] + paso·(P − mu_norm[c]), 0, 5)·rel` es la hija de v11/v14 (con la máscara de la hija dispersa
cuando hay estadística). **`kj@P > KW[c]@P` es la discrepancia de retina** que v11 ya exige: sólo se cumple si `P` se
aparta de la imagen media `mu[c]` con la que la celda ganó su valor (con `P = mu[c]`, `kj@P = 0.95·KW[c]@P` y no
divide). Por eso: (i) con el mismo estímulo y `R = 0` **no** divide; (ii) con dos estímulos de la **misma** valencia y
el mismo código (4c del examen: C veneno con C∩B = 3) **no** divide, porque `Wb[c]·R > 0` y `R ≠ 0`; (iii) en los
mundos del tronco `R ∈ {+1, −3}`, nunca 0 → **el mecanismo es inerte por construcción** y el organismo con la perilla
encendida es v14.1 **bit a bit** (es la predicción T1/T2 de §5, comprobada además en el arnés como I5).
En el mundo vivo la hija hereda las otras necesidades como en v14.1 (`hereda_nec`); la fisión es sólo de la activa.
Perilla `desambiguar = 0 | 1`; claves nuevas de sólo lectura `des_splits`, `des_t`.

**Por qué éste y no los otros dos del encargo.** *Código extendido a K+1 en colisión*: la cuarta celda lee 0 y la
regla delta sigue empujando las tres compartidas (el veneno se diluye igual); no separa. *K-WTA con desempate por
retina*: los códigos aliados no están empatados, son idénticos; no hay qué desempatar. La división es el órgano que
el tronco ya tiene para separar códigos; lo que le faltaba era una **entrada**: leer `R = 0` como desconfirmación.

## 4. Instrumentos (por anclas; los congelados SÓLO se leen; `construye_codigo.py`)

`organismo_v14_codigo.py` ← `organismo/organismo_v14.py` (feefc88b1fd8d434) · `organismo_v14_codigo_on.py` (perilla
fija en 1; lo examinan las baterías) · `organismo_v14g_codigo.py`/`_on` ← `organismo/organismo_v14g.py`
(1f1318480cd34cde) · `organismo_vivo_codigo.py` ← `experimentos/nivel11_mundo_vivo/organismo_vivo.py`
(20c0961c79de8825) · `bateria_v14_codigo.py` ← `organismo/bateria_v14.py` (72216f5415de0c86) sobre `_on` ·
`bateria_generaliza_codigo.py` ← `organismo/bateria_generaliza.py` (9cf72581ebae7dea), una entrada nueva **con
`eta_s = 0.15, clip_s = 10.0` explícitos** (los mismos kwargs que la entrada del tronco).
Arnés `identidad_codigo.py`: I1 12 escenarios × 2 semillas (T = 30 000) ≡ v14.1 · I2 rng no consumido (T = 120 000)
· I3 mundo de regla 3 × 2 ≡ v14g · I4 mundo vivo 5 montajes × 2 ≡ `organismo_vivo` · I5 (predicción) perilla ON ≡ v14.1
en I1 e I3 · I6 control que DEBE fallar: NO_INFORMA, semilla alias 326, ON ≠ OFF con `des_splits ≥ 1`.
Runner `corre_codigo.py` (subprocesos secuenciales; `--humo` de un proceso).

## 5. Brazos, medidas y criterios (la LETRA; el runner los copia tal cual, ERR-31)

**Mundo vivo, T = 100 000, semillas del bloque de la sal** (ALIAS 326, 334, 343, 377, 446, 533, 549, 563, 670;
LIMPIAS 307, 313, 316, 323, 325, 327, 333, 338, 342; recalculadas al arrancar como en `corre_sal.py`). Base
NO_INFORMA (`vivo=1, n_nec=2, 4 estímulos, costo=costo_a=0.001, sal muda`), 6 brazos × 9 semillas = 54 corridas:

| brazo | semillas | perilla | qué es |
|---|---|---|---|
| D0-ALIAS | ALIAS | 0 | **guarda**: debe reproducir S1-ALIAS de `sal_alias9_20260918_081346` (d521f569205ebcfd) semilla a semilla |
| **D1-ALIAS** | ALIAS | **1** | el candidato |
| D0-LIMPIA | LIMPIAS | 0 | guarda: reproduce S1-LIMPIA |
| D1-LIMPIA | LIMPIAS | 1 | **coste en semillas limpias** (ahí también hay solapamientos parciales y `R = 0` de agua/sal) |
| D1-SINSED | ALIAS | 1 | `n_nec = 1`: **el tronco con cuatro estímulos** |
| D1-VIVO / D0-VIVO | ALIAS | 1 / 0 | sal **informativa** (tabla por defecto): la tabla 2×2 {sal, veneno} × {hambre, sed} debe salir exacta |

Medidas por corrida: `W_nec` (valor por necesidad y estímulo; `|W[sal]|` = máximo sobre las necesidades que existen,
como en `corre_sal.py`), `exposiciones`, `splits`, `des_splits`, `des_t`, `celdas`, `deaths`, `muertes_nec`.

| # | criterio (mundo vivo) | umbral |
|---|---|---|
| **G** | guardas: D0-ALIAS y D0-LIMPIA idénticos al JSON del bloque de la sal en `w_sal`, `w_veneno`, `splits`, `celdas`, `deaths` | **18/18**; si no, el instrumento cambió y se para |
| **C1** | D1-ALIAS `\|W[sal]\| ≤ 0.3` | **≥ 8/9**, mediana ≤ 0.1 |
| **C2** | D1-ALIAS `W_hambre[veneno] ≤ −2.8` | **≥ 8/9**, y ≤ −2.5 en 9/9 |
| **C3** | evitación: exposiciones a la sal de D1-ALIAS ≤ **1.5 ×** la mediana de D1-LIMPIA | ≥ 8/9 (v14.1: ×7) |
| **C4** | causa: `des_splits ≥ 1` en D1-ALIAS y la **primera** división por `R = 0` ocurre en una mordida de **D** | 9/9 y ≥ 8/9 |
| **C5** | coste: D1-ALIAS y D1-LIMPIA `celdas ≤ 45` (el presupuesto del examen) | 18/18; mediana de celdas ≤ 40 |
| **C6** | no regresión en limpias: D1-LIMPIA `\|W[sal]\| ≤ 0.3` y `W_hambre[veneno] ≤ −2.8` | **9/9 y 9/9** |
| **C7** | el tronco con 4 estímulos: D1-SINSED cumple C1 y C2 | ≥ 8/9 cada uno |
| **C8** | tabla 2×2 en D1-VIVO: `\|W_h[sal]\| ≤ 0.3`, `W_s[sal] ≤ −2.5`, `W_h[ven] ≤ −2.8`, `\|W_s[ven]\| ≤ 0.3` (las cuatro a la vez) | ≥ 7/9; y en D0-VIVO la tabla **falla** en ≥ 7/9 (el alias está en las dos filas) |
| **C9** | supervivencia (medianas, no pareado: ERR-37b): muertes D1-ALIAS ≤ **0.8 ×** D0-ALIAS | sí/no; se reporta A₁₂ |

**Tronco** (lo que el candidato NO puede costar):

| # | criterio | umbral |
|---|---|---|
| **T1** | examen v3′ `bateria_v14_codigo.py 20 --desde 101 --log` (perilla ON) | **8/8**, y las listas `splits` por etapa **idénticas** a las del examen de v14.1 en 101–120 (`examen_v14_e015c10_20260918_053452.log`, cuyo organismo es v14.1 semilla a semilla: sus 40 corridas de generalización coinciden con las de feefc88b) |
| **T2** | `bateria_generaliza_codigo.py organismo_v14_codigo_on 20 --desde 101 --log` | **G1 ≥ 0.80, G2 ≥ 0.85, K 20/20**, y `acc`/`ba`/`splits`/`celdas`/`deaths` **idénticos** por semilla y regla a `regresion_generaliza_organismo_v14_20260918_054926.json` (40/40) |
| **T3** | coste en el tronco: celdas, divisiones, muertes | ±10 % → por T1/T2 debe ser **0 %** exacto |

## 6. Predicción numérica (para poder equivocarme) y qué me tumba

- **C1–C2 pasan 9/9**: en la primera mordida de sal sobre celdas consolidadas del veneno, las tres celdas dividen en
  esa misma mordida (las tres cumplen `|Wb| > 0.2`, `R = 0` y `dist@D ≈ 2·f_B > 0.25`); la sal se queda con hijas de
  valor 0 y el veneno con sus madres. `|W[sal]|` **mediana 0.0**; `W[veneno]` **−3.0** en ≥ 8/9. Fuga posible: una hija
  (ciega fuera de D, pero B comparte 2 de los 3 píxeles de D) entra en el código de B y recibe −3; se resuelve con
  otra división en la siguiente mordida de sal (cada generación pierde 5 % en los píxeles compartidos y gana 0.5·f_B en
  el píxel propio). Por eso predigo `des_splits` **mediana 3–6** y `celdas` **33–38**, no 33 exacto.
- **C3**: exposiciones a la sal de D1-ALIAS **≈ las de las limpias (400–700)**, contra 3 600–4 000 en v14.1.
- **C6 (limpias)**: pasa 9/9. En las limpias hay solapamientos parciales (B–D 2/3 en el 27 % de las semillas, C–D en el
  28 %) y estímulos con `R = 0` (agua y sal para el hambre; comida, veneno y sal para la sed), así que **sí habrá
  divisiones por `R = 0`** en las limpias (predigo `des_splits` mediana 2–8, celdas 32–40) sin tocar el valor del veneno.
- **C7**: igual que C1–C2 (una sola necesidad no cambia el mecanismo: S-5 ya mostró que la sed no es la causa).
- **C8**: la tabla 2×2 sale exacta en ≥ 7/9 con la perilla; en D0-VIVO el alias corrompe las dos filas (hambre: la sal
  hereda del veneno; sed: el veneno hereda de la sal).
- **C9**: muertes de D1-ALIAS **≈ 40–50** (D0-ALIAS 75; limpias 35): el veneno recupera el miedo y la sal deja de
  ocupar el anillo.
- **T1/T2/T3**: **identidad exacta** con v14.1 (inercia por construcción).
- **Me tumba:** C1 con ≥ 2/9 fallos (la fuga no converge o la mordida de sal no llega: entonces hay que medir cuándo
  se muerde la sal por primera vez); C6 con un solo fallo (la división por `R = 0` daña el veneno en semillas limpias:
  coste > beneficio, no es candidato); C5 con celdas > 45 (la cascada de fugas no para: la ceguera parcial de la hija
  no basta cuando los patrones comparten 2 de 3 píxeles → habría que medir `paso` o la máscara, en un preregistro
  nuevo, no aquí); T1/T2 con cualquier diferencia respecto de v14.1 (imposible por construcción: si ocurre, es un
  ERR de instrumento, no un resultado). **No se buscan variantes después de ver los datos**: si cae, cae, y la siguiente
  (división diferida tras `n` mordidas con `R = 0`, o umbral explícito de discrepancia) va en otro preregistro.

## 7. Trampas revisadas, alcance y coste

Canal simétrico: n/a. Acierto sin balancear: no hay acierto, hay valores y conteos con n = 9 y 9. El mundo que se come
la comida: las exposiciones son variable dependiente (C3) y se reportan crudas. Sitios fijos: `spawn()` sortea; las
semillas se eligen por una propiedad del código calculada antes de correr (las mismas del bloque de la sal, rango
301–700; ninguna de 1–200 ni 101–120 se gasta aquí). **Alcance declarado:** el mecanismo sólo actúa con `R = 0`
exacto; en mundos con recompensa ruidosa un `R = 0` fortuito dispararía divisiones (una hija sin valor, reversible
por la regla delta, pero cuesta una celda): ese régimen no existe hoy en el proyecto y no se mide aquí. Tampoco mide
el alias entre estímulos de **magnitud** distinta y el mismo signo (no existe en el tronco: `R ∈ {+1, −3}`). Nueve
semillas por brazo no cierran nada: confirman o refutan este mecanismo y piden réplica con las ALIAS del rango
siguiente (`diagnostico_codigos.py --desde 701`).
**Coste:** T1 ≈ 4 min y T2 ≈ 1 min con `Pool(14)` (medidos hoy para v14.1); los 54 + 18 brazos del mundo vivo ≈ 1 min;
identidad ≈ 3 min en un proceso. Total ≈ 10 min, en subprocesos secuenciales.

## 8. Medido DESPUÉS de escribir §1–§7 (identidad y humo) — NO es la serie; ningún umbral de §5–§6 se ha tocado

**Identidad (`identidad_codigo.py 30000`, un proceso, 149 s): 42/42 exigidas** — I1 24/24 ≡ v14.1 · I2 rng no consumido
(T = 120 000) 2/2 · I3 6/6 ≡ v14g · I4 10/10 ≡ `organismo_vivo` (incluidos los montajes de 4 estímulos y 2 necesidades).
**I5 (predicción de inercia): 30/30** — con la perilla ENCENDIDA el organismo es v14.1 bit a bit en los 12 escenarios del
tronco y las 3 reglas del mundo de regla (R nunca es 0 ahí). **I6 (debe fallar): falla como debe** — semilla alias 326,
T = 40 000: OFF `W_h[veneno] = W_h[sal] = −2.03`; ON `−3.0 / −0.0` con `des_splits = 6`.

**Humo (`corre_codigo.py --humo`, `datos/codigo_humo_20260918_085115` 11aa92b347152063; un proceso, T = 100 000):**

| brazo | semilla | \|W[sal]\| (hambre, sed) | W[veneno] (hambre, sed) | exp. sal | divisiones (por R=0) | celdas | muertes |
|---|---|---|---|---|---|---|---|
| D0-ALIAS (v14.1) | 326 | **1.80** (−1.80, 0.0) | **−1.80** (−1.80, 0.0) | 4 009 | 0 (0) | 30 | 90 |
| **D1-ALIAS** | 326 | **0.00** (−0.0, 0.0) | **−3.00** (−3.0, −0.0) | **556** | 6 (6) | 36 | **38** |
| D0-LIMPIA (v14.1) | 307 | 0.00 | −3.00 | 555 | 0 (0) | 30 | 31 |
| D1-LIMPIA | 307 | 0.00 | −3.00 | 555 | 3 (3) | 33 | 31 |
| D1-SINSED (tronco con 4 estímulos) | 326 | 0.00 | −2.88 | 374 | 6 (6) | 36 | 41 |
| D1-VIVO (sal informa la sed) | 326 | W_h 0.0 · **W_s −3.0** | **W_h −3.0** · W_s 0.0 | 1 567 | 9 (9) | 39 | 83 |

Las guardas G reproducen el bloque de la sal (D0-ALIAS 326 y D0-LIMPIA 307 idénticos a S1-ALIAS/S1-LIMPIA). Las tres
primeras divisiones por `R = 0` caen **en la misma mordida de D** (t = 424), como decía §6; la cuarta es de C (agua, `R = 0`
para el hambre, código parcialmente compartido) y las dos siguientes de D otra vez (la fuga de la hija al código de B,
resuelta). En la semilla limpia el valor no se mueve y cuesta 3 celdas. Con una semilla no se decide nada: la serie
decide con los umbrales de §5 tal como están escritos.


## Enmienda 1 (coordinador, 18 sep 09:12 — réplica automática por la regla 12; escrita ANTES de correrla; ningún umbral cambia)

Serie 1 (`codigo_alias9_20260918_085958`): G 18/18, C1–C3 y C5–C9 pasan, T1–T3 identidad exacta con v14.1; **C4 7/9** (se exigía ≥ 8/9):
a una semilla del umbral → réplica en semillas nuevas. Semillas elegidas estructuralmente antes de correr con
`diagnostico_codigos.py --desde 701 --n 400 --alias 3`: **ALIAS** (las 9 primeras con `|code(D) & code(B)| = 3` en 701–1100) = 779, 796,
822, 852, 895, 916, 917, 926, 944; **LIMPIAS** (las 9 primeras con `|D & B| = 0`) = 703, 712, 717, 725, 728, 744, 746, 751, 764. Mismos brazos,
kwargs y umbrales (runner `corre_codigo_replica.py`, que reutiliza las funciones de `corre_codigo.py`). T1/T2 no se repiten (inercia
exacta medida en la serie 1). La guarda G no aplica a semillas nuevas; en su lugar **G′**: D0-ALIAS `|W[sal]| > 0.3` en ≥ 8/9 y D0-LIMPIA
`≤ 0.3` en 9/9 (si no, las semillas no reproducen el alias y no se interpreta). **Veredicto de la réplica:** PASA si G′ y C1, C2, C3, C5,
C6, C7, C8, C9 pasan; C4 se reporta con su letra. Si la réplica pasa y C4 vuelve a quedar en 7/9, el mecanismo se declara con el
vocabulario provisional y C4 se reescribe en un preregistro futuro como criterio de causa (no de dónde cae la primera división).
