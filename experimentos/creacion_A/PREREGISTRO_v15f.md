# PREREGISTRO — candidato **v15f**: tabla de pares con **R crudo + sobrescritura + relevo a la lineal**, cada vía con su error

CREADOR A, 18-sep-2026 (09:50). Lo corre el coordinador (`corre_v15f.py`). **§1–§7 escritos ANTES de medir nada; §8 (humo) se
mide después y se dice.** Sin `Pool` por mi parte (hay una sala de agentes trabajando), sin commits, nada congelado tocado,
nada de v15c/d/e sobrescrito.

**Misión (primero):** llegar a la AGI por este camino — un organismo mínimo con reglas locales que aprende sin morder de más,
**generaliza Y se desdice** cuando el mundo cambia. v15e demostró en 20 semillas que la vía lenta puede acertar a la primera y
desdecirse en una mordida (E1 W_B ≈ −3 20/20; E2 reversión 20/20); perdió XOR porque guardaba residuos. v15f conserva lo
primero y devuelve a la tabla lo que identificaba XOR: **R crudo**.

## 1. De dónde viene (medido, no hipótesis)

| candidato | tabla guarda | lectura lenta | lineal aprende de | E1 W_B≈−3 | E2 reversión | V2b xor01 estricta | gana (0,1) |
|---|---|---|---|---|---|---|---|
| v15c | R crudo, un golpe + EMA .3 | tabla (0 si no vio) | R − tabla | (no medido ON) | (no medido ON) | 0.812 | 20/20 |
| v15d `suma` | R crudo, un golpe + EMA .3 | lineal + tabla | R − (lineal + tabla), ANTES de escribir | **0/20** | **0/20** | 0.875 | 20/20 |
| v15e | **residuo** R − lineal, sobrescritura | lineal + residuo | R − lineal | **20/20** | **20/20** | **0.500** | 20/20 (al final; en la sonda gana otra) |

Lo que enseña la fila de v15e (`datos/v15e_s141-160_20260918_092921`, `examen_v15e_20260918_093053`): la exactitud a la primera
y la reversión en una mordida **no dependen del residuo** sino de que la tabla escriba **después** de la lineal y **sobrescriba**,
y de que la boca lea R exacto (no 1.45·R). La identificabilidad del par (0,1) **sí** depende de que la casilla guarde R crudo: con
residuos el error propio de la celda buena es la deriva de una lineal que no puede con XOR (`diagnostico_xor_v15e.py`: gana (2,4)
en la sonda, 9/12 signos mal). v15f separa las dos cosas.

## 2. Hipótesis

**H15f.** Si la tabla guarda **R crudo** por sobrescritura y la vía lenta **releva** (la casilla de la celda ganadora si conoce la
combinación; si no, la lineal), con **cada vía aprendiendo de su propio error**, entonces (i) la boca lee R exacto tras UNA
mordida y se desdice en UNA (lo de v15e), (ii) el prior de pares recupera la identificabilidad de M3/v15c/v15d en XOR, y (iii)
la lineal de v14.1 sigue intacta para las combinaciones que la tabla no vio.

## 3. Mecanismo y decisiones (tomadas ANTES de medir)

Perilla `memoria_pares = None | 'relevo'`, `mem_alfa = 1.0`, `mem_rho = 0.02`. Estado: 60 casillas + 60 visitas + 15 errores = 135.

- **D1 — vía rápida: SU propio error** `dlt = R − _wf` (línea de v14.1 sin tocar).
- **D2 — lineal: SU propio error** `_ds = R − lineal(P)` (apagada: la misma expresión que `R − _ws`, bit a bit). La lineal aprende
  como en v14.1 aunque la boca no la lea: es la que contesta cuando la tabla no conoce la combinación.
- **D3 — tabla:** 15 celdas (pares) × 4 casillas; en cada mordida las 15 escriben **R crudo** (sobrescritura, `mem_alfa = 1.0`).
- **D4 — relevo (la lectura de la vía lenta):** `tabla(P)` si la casilla de la ganadora para P se vio; **si no, `lineal(P)`** —
  la abstención cae hacia la lineal, no hacia 0.0 (en v15c caía a 0.0: por eso en px0 daba 0.900 con 1.000 alcanzable).
- **D5 — celda ganadora:** menor error propio **de la casilla sola** (`R − casilla`, 0.0 si no vista: el criterio de M3 que
  identificó (0,1) 19–20/20), EMA `mem_rho`; desempate al azar con el rng del organismo; sólo consume rng con la perilla ON y
  empate real.
- **D6 — puerta de v14.1 intacta:** rápida si familiar, si no la lenta (= relevo). `None` ≡ v14.1 bit a bit sin consumir rng.
- **Qué NO hay:** suma, residuos, umbral de sobrescritura, decaimiento de la tabla, modos intermedios.

**Es un segundo relevo dentro de la vía lenta, simétrico a la puerta de v13:** *exacto si lo conoce, regla si no* — y las dos
memorias aprenden siempre, cada una de lo suyo.

## 4. Instrumentos (por anclas; congelados sólo leídos; `manifiesto.py --check` 16/16 tras construir)

`construye_v15f.py` → `organismo_v15f.py` (96fc5c5262107850) ← `organismo/organismo_v14.py` (feefc88b1fd8d434) ·
`organismo_v15f_on.py` (54d6efe0b564113c) · `organismo_v15gf.py` (e4c4e0b00b1c20e3) / `_on` (039eee1bba9ebdf0) ←
`organismo/organismo_v14g.py` (1f1318480cd34cde) · `bateria_v15f.py` (d63f5aee558eb6da) ← `bateria_v14.py` (72216f5415de0c86)
sobre `_on`, sha de v11/v10 desde `organismo/` (JSON del examen siempre escrito) · `bateria_generaliza_v15f.py` (0cd87d2632e0c66a) ←
`bateria_generaliza.py` (9cf72581ebae7dea), entrada nueva **verificada campo a campo** con la del tronco por el constructor (regla 14)
· `identidad_v15f.py` · `corre_v15f.py`: identidad → V1 → V2a → V2b 161–180 (kwargs exactos del tronco), subprocesos secuenciales;
**lee los veredictos y las corridas de los JSON que escriben las baterías, no del log** (ERR-43: el runner de v15e reconstruía el
azar del log con una regex codiciosa y leyó 20.000); `--humo` de un proceso.

## 5. Criterios (escritos antes de la serie; semillas: examen y generalización 101–120, mundo de regla 161–180)

- **V1 — examen v3′ 8/8 en 101–120, perilla ENCENDIDA.** Lo que mata, explícito: E1 **"W_B ≈ −3"** (|W_B + 3| < 0.3) y E2
  **reversión** ("W_A → −3", "W_B → +1", "come B Q4 ≥ 50"), 20/20 cada uno, a la letra de la batería. También a la letra: E1
  "veneno Q4 < Q1" (v15e: 19/20) y E2I "W_C ≤ −2.5" (v15e: 19/20) — los dos subcriterios donde v15e perdió una semilla; si v15f
  pierde una ahí, se aplica la regla 12 de EQUIPO (réplica en rango nuevo la decide el coordinador), no una enmienda.
- **V2a — generalización ON** (`bateria_generaliza_v15f.py organismo_v15f_on 20 --desde 101 --log`): **G1 ≥ 0.80, G2 ≥ 0.85,
  K 20/20**, con `azar` de G1 en [0.35, 0.65] y de G2 en [0.42, 0.58] (las bandas de la batería), leídos del JSON.
- **V2b — mundo de regla 161–180, pareado ON/OFF, kwargs exactos del tronco:** `xor01` **ESTRICTA mediana ≥ 0.75**; `azar` ∈
  **[0.35, 0.65]**; `px0` **mediana ON (registro) ≥ mediana OFF**. Se reportan al lado: pareado por semilla, `gana (0,1)`, cobertura.
- **V4 — coste:** `celdas` y `splits` (medianas, xor01 y px0) dentro de **±10 %** de OFF; muertes pareadas. **Declaro:** en v15e
  xor01 dio celdas +9 %, splits +18 %; espero lo mismo o menos aquí (la boca lee R exacto y muerde menos veneno; las divisiones
  extra de v15e venían de una lineal + residuo que a veces decía "comida" a un veneno). Regla fijada: **por abajo no refuta; por
  arriba (+10 %) cuenta como coste** que el coordinador pesa. Aparte, no decide la entrada.
- **V3 `n*`:** no medible con estos instrumentos; no es criterio.

## 6. Predicción numérica (para poder equivocarme)

- **V1: 8/8.** E1 W_B −3.0 ± 0.1 en 20/20 (tabla exacta con la puerta cerrada; rápida consolidada cuando se abre: v15e dio 20/20
  con la misma exactitud a la primera); E1 "veneno Q4 < Q1" 19–20/20 (**riesgo declarado**: con −3 desde la primera mordida Q1 tiene
  pocas mordidas y Q4 puede empatar; v15e 19/20). E2 reversión 20/20 × 3 (como v15e). E2I "W_C ≤ −2.5": 20/20 — en v15f C lee
  **su propia casilla** (R crudo −3) en cuanto se muerde una vez, y si su casilla colisiona con la de A la celda ganadora cambia
  en la siguiente mordida de A (error 16 contra 0); en v15e ese caso leía lineal + residuo ajeno. E2J/E2K/E2L 20/20. 3′ 0/20; 3″
  ≥ 19/20; 2, 4a–4d pasan.
- **V2a: G1 1.000** (azar 0.40–0.60, px0 > azar ≥ 18/20), **G2 ≥ 0.97**, K 20/20. Casilla vista → R de la última con esa
  combinación (correcto si la ganadora contiene el píxel 0: en px0 las 5 celdas con píxel 0 tienen error 0 y las otras 10 se
  confunden); casilla no vista → la lineal de v14.1 (mejor que el 0.0 de v15c).
- **V2b (kwargs del tronco): xor01 estricta ON 0.81** [0.69, 1.00] (v15c 0.812, v15d 0.875; techo por alias de código de la
  puerta: los test familiares leen la rápida); `gana (0,1)` ≥ 18/20; OFF ≈ 0.44. **px0 ON = OFF = 1.000** (mediana). **azar 0.50 ± 0.05.**
- **V4:** xor01 celdas dentro de ±10 %; splits **puede pasar de +10 %** (v15e +18 %): lo declaro como el sitio donde espero pagar.
- **Lo que me tumba (y qué diría):** (a) xor01 < 0.75 → el relevo no basta para XOR: la tabla necesita la lineal fuera de la boca
  y aun así los alias de la puerta comen el margen; se reporta como techo del prior de pares dentro del tronco (0.81 en dos
  candidatos anteriores dice que no pasará, pero la letra manda). (b) px0 < OFF → la ganadora sin píxel 0 tapa a la lineal en
  ≥ 3/20 semillas: el precio del relevo frente a la suma; entonces el diseño correcto pasa por dejar que la lineal vote donde la
  tabla está insegura — **eso sería otro candidato con preregistro nuevo, no una enmienda**. (c) E1 W_B ≈ −3 o E2 < 20/20 → la
  exactitud a la primera no es suficiente sin la lineal en la lectura (contradiría a v15e; lo dudo). (d) E1 "veneno Q4 < Q1" 19/20
  → regla 12, réplica, no enmienda. (e) `azar` fuera de banda → fuga.

## 7. Cláusula

Si **V1** o **V2a** caen, v15f **no entra al tronco**; si V2b `xor01` o `azar` caen, tampoco. **Sin modos intermedios ni dosis
después de ver los datos**; `mem_alfa = 1.0` y `mem_rho = 0.02` quedan fijados aquí. Todo cambio de umbral tras ver datos lleva
ERR numerado (libres desde ERR-44, los numera el coordinador; este preregistro no necesita ninguno). Semillas fijas: 101–120 (V1,
V2a) y 161–180 (V2b).

## 8. Humo (UN proceso, T ≤ 200 000, ≤ 3 semillas, sin Pool) — medido DESPUÉS de escribir §1–§7

`corre_v15f.py --humo`: (a) E1 y E2 (semillas 101, 102; T = 100 000) para **v14.1 (off)**, **v15e** (el candidato anterior) y **v15f**,
con W, lineal, casilla (R crudo), rápida (Wp, Wn), puerta y mordidas por trimestre; (b) mundo de regla, semilla 141, xor01 / px0 /
azar, **v15f ON, OFF (= v14.1) y v15e ON** pareados con los kwargs del tronco. Lo que el humo NO puede decir: nada sobre 20 semillas.

**Medido (09:47–09:58; `datos/v15f_humo_20260918_094706.{log,json}`, json 84b79f7cd56f0088; un proceso, 12 + 9 corridas):**
identidad **32/32** (I1 24/24 · I2 2/2 · I3 6/6). I4: ON con `puerta_pat=5` sin excepción; la tabla lee R crudo (A +1.0, B −3.0;
C no vista → lineal).

| escenario (T = 100 000) | organismo | W_A | W_B | lineal B | tabla B | rápida B (Wp, Wn) | B familiar | mordidas B por trimestre | letra |
|---|---|---|---|---|---|---|---|---|---|
| E1 s101 | v14.1 (off) | +1.00 | −2.96 | −3.00 | — | (0, 2.96) | sí | [27, 11, 8, 1] | pasa |
| E1 s101 | v15e | +1.00 | −2.97 | −3.00 | (residuo 0) | (0, 2.97) | sí | [15, 20, 5, 9] | pasa |
| E1 s101 | **v15f** | +1.00 | **−2.94** | −3.00 | **−3.00** | (0, 2.94) | sí (ev 41) | **[2, 16, 14, 9]** | W_B ≈ −3 sí · **veneno Q4 < Q1 NO** |
| E1 s102 | v14.1 (off) | +1.00 | −2.98 | −3.00 | — | (0, 2.98) | sí | [27, 9, 7, 8] | pasa |
| E1 s102 | **v15f** | +1.00 | **−2.96** | −3.00 | **−3.00** | (0, 2.96) | sí (ev 45) | [11, 17, 8, 9] | pasa |
| E2 s101 | v14.1 (off) | −2.95 | +1.00 | +1.00 | — | (1.0, 0) | sí | [27, 11, 96, **81**] | pasa |
| E2 s101 | **v15f** | **−2.82** | **+1.00** | +1.00 | **+1.00** | (1.0, 0) | sí | [2, 16, 78, **95**] | **pasa las tres** |
| E2 s102 | v14.1 (off) | −2.90 | +1.00 | +1.00 | — | (1.0, 0) | sí | [27, 9, 84, 90] | pasa |
| E2 s102 | **v15f** | **−2.87** | **+1.00** | +1.00 | **+1.00** | (1.0, 0) | sí | [11, 17, 87, **78**] | **pasa las tres** |

| mundo de regla s141 (kwargs del tronco, T = 200 000) | **v15f ON** registro / ESTRICTA | ba | ganadora | OFF (= v14.1) | v15e ON | celdas / splits (ON · OFF) |
|---|---|---|---|---|---|---|
| **xor01** | **1.000 / 1.000** | 0.999 | **(0,1)**, 4/4 | 0.375 | 0.250 | 55 / 25 · 69 / 39 |
| px0 | **1.000 / 1.000** | 0.999 | (0,1) | 1.000 | 1.000 | 48 / 18 · 51 / 21 |
| azar | 0.400 / 0.400 | 0.401 | (1,3) | 0.800 | 0.600 | 67 / 37 · 62 / 32 |

**Lo que el humo confirma:** (i) la exactitud a la primera y la reversión en una mordida se conservan con R crudo (tabla B −3.00,
E2 +1.00 exacto, come B Q4 78–95); (ii) **el prior de pares recupera XOR** en la semilla donde v15e lo perdió (1.000 contra 0.250,
ganadora (0,1)); (iii) px0 = OFF; azar en banda (0.400; OFF 0.800 en esa semilla, una semilla). (iv) V4 en la dirección declarada
(xor01 celdas −20 %, splits −36 %: menos, no más).

**Lo que el humo avisa — riesgo (d) de §6, más grande de lo que escribí:** E1 s101 **"veneno Q4 < Q1" NO** (Q1 2, Q4 9; s102 sí:
11 contra 9). El mecanismo: con −3 exacto desde la PRIMERA mordida, Q1 casi no tiene mordidas (2); la puerta se abre en Q2 (5
mordidas) y la rápida, que lee −1.13, consolida en Q2–Q4 con las mordidas que v14.1 daba en Q1 (v14.1: 27 en Q1). El total de
mordidas de veneno es **menor** (41–45 contra 47–51 de v14.1), pero el criterio de la batería mide **dónde caen**, no cuántas, y
está escrito para un organismo que aprende en 5–27 mordidas. **No cambio la letra** (sería un ERR de umbral tras ver datos):
predicción actualizada tras el humo (dicha, no preregistrada): V1 **E1 "veneno Q4 < Q1" 15–18/20** → **V1 cae por ese subcriterio**
con W_B ≈ −3 20/20 y E2 reversión 20/20; V2a pasa; V2b xor01 **0.85–0.95** con gana (0,1) ≥ 18/20 y azar en banda. Si la serie sale
así, el coordinador y el director tienen una decisión de criterio, no de mecanismo: *"un organismo que aprende el veneno en una
mordida no puede morderlo más en Q1 que en Q4"*. Yo no la tomo (regla 3): la anoto como **candidato a ERR-44** para ellos.
