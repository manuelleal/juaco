# PREREGISTRO — candidato **v15e**: la tabla de pares REESCRIBIBLE, **sin doble cuenta**

CREADOR A, 18-sep-2026. Lo corre el coordinador (`corre_v15e.py`). **§1–§7 se escribieron ANTES de medir nada; §8 (humo)
se mide después y se dice.** Sin `Pool` por mi parte, sin commits, nada congelado tocado, nada de v15c/v15d sobrescrito.

**Misión (primero):** llegar a la AGI por este camino — un organismo mínimo con reglas locales que aprende sin morder de
más, generaliza y **se desdice cuando el mundo cambia**. v15d generalizó y cruzó XOR con 8 ejemplos pero **no se desdijo**
(E2 0/20) y dejó a la vía rápida sin consolidar (E1 0/20). v15e es el candidato nuevo que ataca exactamente eso, con
preregistro nuevo, como exige el §6 de v15d.

## 1. Diagnóstico mecánico de v15d: por qué E2 no revierte y por qué E1 no consolida W_B

Líneas de `experimentos/creacion_A/organismo_v15d.py` (f2f0b06e31877e96; `_on` e57d0677cdff3906), modo `'suma'`:

- **L116** `_ws=_lenta_v15(PAT[kk])` → la vía lenta lee **lineal + tabla** (la tabla abstiene con 0.0 si la casilla no se vio).
- **L132** `_ds=dlt if puerta is None else R-_ws` → la lineal aprende del **error de la SUMA**, calculado **antes** de que la
  tabla escriba en esa misma mordida.
- **L133–L146** en la misma mordida las 15 celdas escriben: primera vez **de un golpe** `_MMv[_cv,_dv]=R` (**L142**); después
  EMA 0.3 (**L143**).
- **L147–L149** `Wps/Wns += 0.15·_ds·P` → con 3 píxeles activos la lectura lineal del patrón se mueve **0.45·_ds**.

**Primera mordida de un patrón nuevo** (lineal 0, casilla vacía): `_ds = R`; lineal → 0.45·R; tabla → R; **la vía lenta
lee 1.45·R**. Para B: **−4.35**. Está medido: en E2I-misma (log `examen_v15d_20260918_083108`, criterio 4c) **W_C mediana
−4.38 con 1 mordida de C en Q3+Q4** — el 1.45·(−3) del cálculo.

**Por qué E1 no consolida W_B.** La boca (**L118**) lee `Vb = 1.2·_wt + 2·hambre + 0.5`: con `_wt = −4.35` y hambre 1,
`pb = 1.1e−4`; con −3, `pb = 0.025`: **220 veces menos mordidas de B**. Las mordidas siguientes son las que corregirían el
exceso (`_ds = −0.45R` → la suma baja ×0.55 por mordida) y **no llegan**: W_B se congela en ≈ −4.35 → |W_B + 3| = 1.35 > 0.3
→ **"W_B ≈ −3" 0/20**, mientras la conducta "veneno Q4 < Q1" pasa 17/20 (una o dos mordidas en Q1, cero en Q4). **La vía
rápida nunca descontó la tabla** (**L130** `dlt=R-_wf`, su propio error, línea de v14.1): lo que le falta no es error, son
**MORDIDAS**. Con 1–2 mordidas de B, `Wn = 0.09–0.17` por celda → ninguna celda consolidada (|Wb| ≤ 0.2) y `ncod[B] < 5` →
la puerta por código no se abre nunca → la boca sigue leyendo la lenta (−4.35) toda la corrida. El diagnóstico del
coordinador ("deja de recibir error") es correcto en el efecto y hay que precisarlo en la causa: **deja de recibir mordidas**.

**Por qué E2 no revierte.** Tras `invertir_en = 50 000`, B es comida y sigue leyéndose −4.35 por la lenta (B nunca fue
familiar): nadie la muerde → "come B Q4 ≥ 50" 1/20 y "W_B → +1" 1/20. A sí es familiar (cientos de mordidas): la rápida
desaprende con su error como en v14.1 y, al cruzar |Wb| < 0.2, la puerta se cierra y la boca lee **lineal + tabla**: la
tabla baja hacia −3 por EMA 0.3 (−3 → −0.2 → −1.04 → −1.63 …) y la lineal, con el error de la suma, se lleva el resto
(`_ds = −3 − (lineal + tabla)`: −4 en la primera mordida tras el cambio → −1.8 de golpe): **las dos bajan a la vez** y la
suma se pasa de −3; cuando la suma es < −3 la boca deja de morder A y el exceso se congela → "W_A → −3" 0/20.

**La reescritura sola no lo arregla** (`mem_alfa = 1.0` sobre v15d): el exceso nace en la **primera** escritura (1.45·R) y se
congela por falta de mordidas; en E2 B sigue en −4.35 y nadie la muerde. Se muestra en el humo (§8) con ese brazo.

## 2. Hipótesis

**H15e.** La memoria de pares entra en la vía lenta **sin doble cuenta** si (i) cada vía aprende de **su propio** error y
(ii) la tabla escribe **después** del paso de la lineal **el residuo que ésta deja**, por sobrescritura. Entonces la vía
lenta lee **exactamente R tras UNA mordida**, **se desdice en UNA mordida** cuando R cambia, y la vía rápida recibe las
mordidas que necesita (las mismas que en v14.1 a lectura −3: `pb = 0.025` con hambre).

## 3. Mecanismo y decisiones (tomadas ANTES de medir)

Perilla `memoria_pares = None | 'suma'`, `mem_alfa = 1.0`, `mem_rho = 0.02`.

- **D1 — vía rápida: SU propio error** `dlt = R − _wf` (línea de v14.1, sin tocar). Razón: nunca fue el problema (§1); con el
  error compartido dejaría de aprender en cuanto la tabla explicara R → E1 moriría con seguridad. Local: sólo ve R y su
  propia lectura.
- **D2 — lineal: SU propio error** `_ds = R − lineal(P)` (con la perilla apagada es la **misma expresión** que `R − _ws`, bit a
  bit). Razón: la lineal debe seguir convergiendo a la regla con las repeticiones (la generalización de v14.1); con el error
  de la suma se congelaría en su primera huella de 0.45·R, que con −3/+1 desequilibrados es junk.
- **D3 — tabla: 15 celdas (pares de píxeles) × 4 casillas.** Tras el paso de la lineal, **cada casilla ← `R − lineal_después(P)`**
  (SOBRESCRITURA: `mem_alfa = 1.0`; el parámetro EMA existe por si el coordinador quiere otra dosis, **el candidato es 1.0**).
  Así la suma lee R exacto y la casilla **sigue a la última recompensa**. Abstención: 0.0 en casillas no vistas → la lectura es
  la lineal sola. Local: la celda ve R y la lectura lineal en la boca.
- **D4 — celda ganadora:** menor error propio (EMA `mem_rho`; error propio de la celda = R − (lineal previa + su casilla));
  **desempate al azar con el rng del organismo**; sólo consume rng cuando la perilla está ENCENDIDA y hay empate de verdad.
- **D5 — lectura:** `_ws = lineal + tabla` en la boca (L116) y en `valor()`; la puerta de v14.1 intacta (rápida si familiar,
  si no la lenta).
- **D6 — `memoria_pares=None` ≡ v14.1 bit a bit sin consumir rng** (I1 24/24, I2 2/2, I3 6/6 en `identidad_v15e.py`).
- **Estado:** 60 residuos + 60 visitas + 15 errores = **135 números** (v15d: 136; no hay `ruta`: v15d mostró que enrutar ≡
  sustituir en px0).
- **Qué NO hay:** modos intermedios, umbral de sobrescritura, decaimiento de la tabla, cambio en la rápida, la puerta o la hija.

**Qué cambia respecto a v15d en una frase:** *en v15d las dos partes de la vía lenta perseguían R a la vez sobre el mismo error
(1.45·R en una mordida); en v15e la lineal persigue R sola y la tabla guarda lo que a la lineal le falta, después de su paso.*

## 4. Instrumentos (por anclas; los congelados SÓLO se leen; `manifiesto.py --check` 16/16 tras construir)

`construye_v15e.py` → `organismo_v15e.py` (5930c5ed2df1be1d) ← `organismo/organismo_v14.py` (feefc88b1fd8d434) ·
`organismo_v15e_on.py` (c576d0de467d7cca, perilla fija `'suma'`) · `organismo_v15ge.py` (e902fb3503655a47) / `_on`
(7d638015ddce4f1c) ← `organismo/organismo_v14g.py` (1f1318480cd34cde) · `bateria_v15e.py` (d5039d16ce21920d) ←
`organismo/bateria_v14.py` (72216f5415de0c86), **sobre `organismo_v15e_on`** · `bateria_generaliza_v15e.py`
(b01142827847c7d7) ← `organismo/bateria_generaliza.py` (9cf72581ebae7dea), entrada nueva **comparada campo a campo por el
constructor con la entrada `'organismo_v14'`** (regla 14 / ERR-38: `eta_s=0.15, clip_s=10.0` explícitos) · `identidad_v15e.py` ·
`corre_v15e.py` (subprocesos SECUENCIALES: identidad → V1 → V2a → V2b; nunca dos `Pool`; `--humo` de un proceso).

Dos diferencias de instrumento respecto a v15d, declaradas (ninguna toca un umbral):
1. **`bateria_v15e` lee el sha de `organismo_v11/v10` en `organismo/`.** La copia de v15d (y la de v15c) hacía
   `h16(os.path.join(AQUI, 'organismo_v11.py'))` con `AQUI = creacion_A/`, donde ese archivo no existe: excepción tras el
   veredicto → **por eso el examen de v15c/v15d no escribió su JSON** (no es que la batería congelada no lo escriba al fallar:
   la línea `datos ->` falta también en `examen_v15c_20260918_080012.log`). Candidato a nota de instrumento del coordinador.
2. **V2b corre el mundo de regla con los kwargs EXACTOS de la entrada del tronco** (`eta_s=0.15, clip_s=10, puerta=3,
   mask_rel=2, del_s=del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1`), así **apagada ≡ v14.1** en ese mundo. El
   runner de v15c/v15d pasaba sólo `eta_s=0.15, puerta=3` (el gemelo dejaba `clip_s=3.0, mask_rel=0, puerta_pat=0`: una
   configuración tipo v13): su ON/OFF pareado es válido en sí, pero **sus números no son comparables 1:1 con los de aquí**
   (regla 14 aplicada también al runner). Lo digo antes de correr. **Lo numero como ERR-41 (propuesto por A, el número que
   el coordinador dejó libre; lo ratifica él):** *"el V2b de v15c y v15d (`corre_v15c.py`, `corre_v15d.py`) midió el mundo
   de regla en una configuración tipo v13 (clip_s 3.0, sin hija dispersa ni puerta por código), no en v14.1: su `px0 ≥
   apagada` y su V4 se leen contra ESA base, no contra el tronco"*. No cambia ningún umbral ni el veredicto de v15d (que
   cayó por V1).

## 5. Criterios (escritos antes de la serie; semillas: examen y generalización 101–120, mundo de regla 141–160)

- **V1 — examen del criterio v3′, 8/8 en 101–120, perilla ENCENDIDA** (`bateria_v15e.py 20 --desde 101 --log`). **Lo que
  mata al candidato, explícito:** E1 **"W_B ≈ −3"** (|W_B + 3| < 0.3) y E2 **reversión** ("W_A → −3", "W_B → +1", "come B
  Q4 ≥ 50"), a la letra de la batería (20/20 cada uno). Un 19/20 en el umbral dispara la regla 12 de EQUIPO (réplica en rango
  nuevo, la decide el coordinador), no una enmienda.
- **V2a — generalización con la perilla ON** (`bateria_generaliza_v15e.py organismo_v15e_on 20 --desde 101 --log`):
  **G1 ≥ 0.80, G2 ≥ 0.85, K 20/20** (la letra del coordinador; la batería imprime sus umbrales propios 0.65/0.55 y el runner
  lee los medianos y aplica los de aquí, los estrictos).
- **V2b — mundo de regla 141–160, pareado ON/OFF con los kwargs del tronco:** `xor01` **ESTRICTA mediana ≥ 0.75**; `px0`
  **mediana ON (registro) ≥ mediana OFF**; `azar` mediana ON ∈ **[0.35, 0.65]**. Se reporta al lado el pareado por semilla
  (ON ≥ OFF en px0) y `gana (0,1)` en xor01.
- **V4 — coste:** `celdas` y `splits` (medianas, xor01 y px0) dentro de **±10 %** de OFF; muertes pareadas. **Declaro que
  espero incumplirlo POR ABAJO en xor01** (−10 a −20 %: la boca deja de morder veneno tras una mordida → menos conflictos →
  menos divisiones; v15d: −18 %). Regla que fijo ahora: **por abajo no refuta** (es menos gasto, en la dirección de la
  misión); **por arriba (+10 %) cuenta como coste** que el coordinador pesa contra el candidato.
- **V3 `n*`:** no medible con estos instrumentos (como en v15d); no es criterio.

## 6. Predicción numérica (para poder equivocarme)

- **V1: 8/8.** E1: W_B −3.0 ± 0.1 en 20/20 (por la lenta exacta mientras la puerta está cerrada, por la rápida consolidada
  cuando se abre: la rápida recibe ~200 veces más mordidas que en v15d, las mismas que v14.1 a lectura −3); mordidas de B
  Q1 ≫ Q4 (v15d: 1–2 en total). E2: "come B Q4 ≥ 50" 20/20, "W_B → +1" 20/20, "W_A → −3" 20/20 (la lenta se desdice en una
  mordida; la rápida como v14.1). E2L 20/20 (los 10/20 de v15d eran el exceso −4.35 en el código nuevo de B). E2I/E2J/E2K
  20/20 (como v15d). 3′ 0/20; 3″ ≥ 19/20; 2, 4a–4d pasan.
- **V2a: G1 1.000** (azar 0.40–0.60), **G2 ≥ 0.97**, K 20/20: en nunca vistos con casilla no vista contesta la lineal de
  v14.1; con casilla vista, `R_última + (lineal(P) − lineal(P_última))` ≈ R cuando la regla es lineal y la lineal convergió.
- **V2b (kwargs del tronco): xor01 estricta ON 0.80** [0.69, 1.00] (OFF ≈ 0.44); **px0 ON = OFF** (1.000 o 0.95, la misma
  mediana); **azar 0.50 ± 0.05**; `gana (0,1)` en xor01 ≥ 18/20.
- **V4: xor01 celdas ON ≈ −15 %** respecto de OFF (incumplimiento declarado, por abajo); px0 dentro de ±10 %.
- **Lo que me tumba (y qué diría):** (a) E1 "W_B ≈ −3" < 20/20 → la lectura exacta −3 tras una mordida **mata de hambre a la
  rápida** (0.025 por encuentro no bastan para consolidar en 100 000 pasos): sería un canje real de la arquitectura CLS —
  *el que acierta a la primera no repite* — que se reporta, no se parchea. (b) E2 reversión < 20/20 → la sobrescritura no
  basta porque la puerta lee la rápida y la rápida es lenta: entonces el órgano correcto no está en la vía lenta.
  (c) xor01 estricta < 0.75 → el residuo de una lineal que no puede con XOR ensucia la tabla al generalizar: **la tabla debe
  guardar R crudo** (régimen M3/v15c) y `'suma'` no sirve para XOR; v15e no entra. (d) `azar` fuera de banda → fuga, no prior.
  (e) V2a < 0.80/0.85 → la tabla reescribible rompe la lineal por otro camino que no vi.

## 7. Cláusula

Si **V1** o **V2a** caen, v15e **no entra al tronco**; si V2b `xor01` cae, tampoco (el prior de pares deja de aportar en la
suma). **No se buscan modos intermedios ni dosis después de ver los datos**; `mem_alfa = 1.0` y `mem_rho = 0.02` quedan
fijados aquí. Todo cambio de umbral tras ver datos lleva ERR numerado (ERR-39 y ERR-40 ya están tomados; ERR-41 lo uso yo
en §4 para el defecto del runner V2b de v15c/v15d; cualquier otro lo numera el coordinador).
Semillas fijas: 101–120 (V1, V2a; las del criterio del tronco) y 141–160 (V2b).

## 8. Humo (UN proceso, T ≤ 200 000, ≤ 3 semillas) — medido DESPUÉS de escribir §1–§7

Ver `corre_v15e.py --humo`: (a) E1 y E2 (semillas 101, 102; T = 100 000) para **v14.1 (perilla off)**, **v15d `suma` α = 0.3**,
**v15d `suma` α = 1.0 (reescritura sola)** y **v15e**, con W, lineal, residuo, rápida (Wp, Wn), puerta y mordidas por trimestre;
(b) mundo de regla, semilla 141, xor01 / px0 / azar, ON y OFF pareados con los kwargs del tronco. Lo que el humo NO puede
decir: nada sobre 20 semillas.

**Medido (09:19–09:30; `datos/v15e_humo_20260918_091900.{log,json}`, json ed8c1f958d491d9b; un proceso, 16 + 6 corridas):**
identidad **32/32** (I1 24/24 · I2 2/2 · I3 6/6 con los kwargs del tronco). I4: ON con `puerta_pat=5` sin excepción; tras las
mordidas, lineal + residuo = ±R exacto (s1: B −2.995 − 0.005 = −3.00; A 0.998 + 0.002 = 1.00).

| escenario | organismo | W_A | W_B | lineal B | residuo B | rápida B (Wp, Wn) | B familiar | mordidas B por trimestre | criterio de la batería |
|---|---|---|---|---|---|---|---|---|---|
| E1 s101 | v14.1 (off) | +1.00 | −2.96 | −3.00 | — | (0.0, 2.96) | sí | [27, 11, 8, 1] | pasa |
| E1 s101 | v15d `suma` α 0.3 | +1.00 | **−4.22** | −1.22 | (tabla −3) | (0.0, **0.27**) | no (ev 1) | **[1, 0, 0, 0]** | **W_B ≈ −3 NO** |
| E1 s101 | v15d `suma` α 1.0 | +1.00 | **−4.22** | −1.22 | (tabla −3) | (0.0, 0.27) | no | [1, 0, 0, 0] | **NO** (idéntico: la reescritura sola no toca la primera escritura) |
| E1 s101 | **v15e** | +1.00 | **−2.97** | −3.00 | −0.00 | (0.0, **2.97**) | **sí** (ev 49) | **[15, 20, 5, 9]** | **pasa** |
| E1 s102 | v14.1 (off) | +1.00 | −2.98 | −3.00 | — | (0.0, 2.98) | sí | [27, 9, 7, 8] | pasa |
| E1 s102 | v15d `suma` α 0.3 / 1.0 | +1.00 | **−3.72** | −0.72 | (tabla −3) | (0.0, 0.52) | no | [1, 0, 1, 0] | **NO** |
| E1 s102 | **v15e** | +1.00 | **−2.99** | −3.00 | −0.00 | (0.0, 2.99) | **sí** (ev 58) | [30, 8, 9, 11] | **pasa** |
| E2 s101 | v14.1 (off) | −2.95 | +1.00 | +1.00 | — | (1.0, 0.0) | sí | [27, 11, 96, **81**] | pasa |
| E2 s101 | v15d `suma` α 0.3 | **−3.75** | **−4.92** | −1.93 | (tabla −3) | (0.0, 0.27) | no | [1, 0, 0, **0**] | **NO / NO / NO** |
| E2 s101 | v15d `suma` α 1.0 | **−3.99** | **−4.55** | −1.55 | (tabla −3) | (0.0, 0.27) | no | [1, 0, 0, **0**] | **NO / NO / NO** |
| E2 s101 | **v15e** | **−2.87** | **+1.00** | +1.00 | 0.00 | (1.0, 0.0) | sí | [15, 20, 82, **95**] | **pasa las tres** |
| E2 s102 | v14.1 (off) | −2.90 | +1.00 | +1.00 | — | (1.0, 0.0) | sí | [27, 9, 84, 90] | pasa |
| E2 s102 | v15d `suma` α 0.3 / 1.0 | −3.75 / −3.99 | −4.91 / −4.53 | −1.91 / −1.53 | (tabla −3) | (0.0, 0.27) | no | [1, 0, 0, 0] | **NO** |
| E2 s102 | **v15e** | **−2.92** | **+1.00** | +1.00 | 0.00 | (1.0, 0.0) | sí | [30, 8, 112, **81**] | **pasa las tres** |

**Lo que el humo confirma de §1–§2:** v15d lee 1.45·R (−4.22 / −3.72 con la lineal congelada en −1.22 / −0.72), muerde B una
vez en 100 000 pasos y la rápida se queda en Wn 0.27–0.52 (no consolida, no familiar); `mem_alfa = 1.0` da el mismo número
(la reescritura no toca la primera escritura). v15e lee −3.00 exacto, la rápida recibe 49–58 mordidas (v14.1: 47–51) y
consolida a −2.97/−2.99 con la puerta abierta; en E2 la lenta se desdice y B se come 81–95 veces en Q4 (v14.1: 81–90),
W_A −2.87/−2.92, W_B +1.00 exacto. **E1 y E2 son la parte que v15e arregla.**

| mundo de regla s141 (kwargs del tronco, T = 200 000) | ON `suma` registro / ESTRICTA | ba | ganadora en la sonda | OFF (= v14.1) | celdas ON / OFF | splits ON / OFF |
|---|---|---|---|---|---|---|
| xor01 | **0.250 / 0.250** | 0.653 | **(2,4)** (al final (0,1)) | 0.375 | 70 / 69 | 40 / 39 |
| px0 | **1.000 / 1.000** | 0.998 | (0,4) | 1.000 | 57 / 51 | 27 / 21 |
| azar | 0.600 / 0.600 | 0.582 | (2,5) | 0.800 | 66 / 62 | 36 / 32 |

**Lo que el humo contradice de §6 — y es la refutación (c), escrita antes:** xor01 ON 0.250 **< OFF 0.375**. Diagnóstico
(`diagnostico_xor_v15e.py 141 xor01`, reproduce la sonda con T = 100 000 y `fase2_en = 99 999`): en la sonda **la celda
ganadora es (2,4), no (0,1)**, con cobertura 4/4; en los 12 patrones de test la lectura total = lineal(P_nuevo) + residuo
guardado por el ÚLTIMO patrón de entrenamiento con esa combinación, y como la lineal no puede con XOR (`Wps−Wns` = [0.31,
0.84, 0.54, −1.60, −1.04, 0.25]) el residuo es ruido de ±1.6 y la lineal del patrón nuevo otro tanto: 9/12 signos mal.
**Causa mecánica:** con la tabla de residuos, el error propio de la celda buena (0,1) ya no es 0 sino `lineal(P_último) −
lineal(P_nuevo)` (la deriva de una lineal que oscila sobre XOR), del mismo orden que el error de confusión de las celdas malas
→ **el prior de pares pierde la identificabilidad que tenía con R crudo** (M3 / v15c / v15d: gana (0,1) 19–20/20). En px0 y en
A/B la lineal ajusta, el residuo es ≈ 0 y la ganadora da igual: por eso E1, E2 y px0 salen bien y XOR no. Una semilla no es
la serie; la serie es la que decide y **los criterios de §5 no se tocan**. Predicción actualizada tras el humo (dicha, no
preregistrada): V1 8/8 y V2a pasan; **V2b xor01 cae** (mediana 0.35–0.50) → por §7 v15e **no entra**. Lo que queda en pie,
medido: *sin doble cuenta y con sobrescritura, la vía lenta acierta a la primera y se desdice en una mordida, y la rápida
consolida igual que en v14.1*. El siguiente candidato legítimo, con preregistro NUEVO (no construido, no medido; propuesto
en el PUENTE A16): **tabla con R crudo + sobrescritura + la lineal sólo por abstención ("relevo"), cada vía con su error** —
conserva lo que v15e arregló (la boca lee R exacto tras una mordida) y devuelve a la tabla la identificabilidad de M3.
