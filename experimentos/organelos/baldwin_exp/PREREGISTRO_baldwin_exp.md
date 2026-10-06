# PREREGISTRO (CONFIRMATORIO) — BALDWIN CON EXPLORACIÓN: probar lo que la regla rechaza deja aprender a la plasticidad (creador Opus, 29-sep-2026)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas). Encargo aprobado por el director (29-sep). **Hipótesis NUEVA con su propio preregistro; NO es un rescate del NO de BALDWIN**
(commit 43f1a6df). Escrito DESPUÉS del arnés de identidad (40/40, números sólo de identidad) y de la calibración de ε (exploración
APAGADA; sec. 4) y ANTES del humo y de toda serie. La letra está en código: `corre_bexp.py`, función `lee()`.

## 1. Hipótesis
En BALDWIN (serie NO: con inversión cada 22 000, todos los brazos 0/20, plásticos incluidos) el auditor halló el mecanismo: la regla
plástica aprende SÓLO tras morder (`_reglas_aprende`), y una regla de rechazo (w ≈ −2.5) inhibe la mordida; por eso nunca recibe la
consecuencia, no se entera de la inversión y el linaje muere de hambre rechazando lo que ya es bueno (en PLAST_V_Pinf, |w − w0| mediano 0).
**H:** si el cuerpo PRUEBA de vez en cuando lo que sus reglas rechazan, pero sólo cuando su reserva aguanta el golpe, la regla plástica
recibe su consecuencia, la plasticidad rescata al linaje en el mundo que cambia (P/vida ≈ 10) y la selección prende el bit plástico.
Explorar sin aprender (FIJO_EXP) NO basta, y el bit sin herencia (AZA) rinde menos.

## 2. Mecanismo mínimo y memoria nueva
- **Memoria nueva: CERO.** Dos constantes del mundo experimental, iguales para todos los cuerpos y todos los brazos EXP (no son genes):
  `th_exp` = 0.5 y `eps_exp` (calibrada, sec. 4).
- **Regla (opción ii del encargo, local, la de O1: "prueba sólo si aguanta el golpe"):** en cada decisión de boca (el cuerpo está sobre
  una letra), si la boca decidió NO morder, la suma de sus reglas de boca activas es NEGATIVA (una regla de rechazo empujó al no) y
  min(E, Ag) ≥ th_exp, entonces con probabilidad eps_exp muerde igual. La mordida exploratoria es REAL: mismo efecto EFF, misma
  R = RV[letra, necesidad], mismo aprendizaje del cerebro; si el cuerpo tiene reglas plásticas de boca, éstas reciben su consecuencia por
  la vía de BALDWIN (Rescorla-Wagner local, eta_s y aversión del propio cuerpo). No se crea ninguna señal nueva.
- **th_exp = 0.5 (fijado a priori):** el peor efecto de una mordida es −0.4 (veneno en E, sal en Ag); con reserva ≥ 0.5 el cuerpo
  sobrevive al peor bocado con 0.1 de margen (100 pasos de costo basal). Los recién nacidos (dote 0.6) ya pueden explorar.
- **Por qué (ii) y no (i) ε heredable:** (i) añade un gen que la selección apagaría en las fases estables (22 000 pasos ≈ 10 vidas sin
  cambio: el mismo valle que mató a BALDWIN) y mezclaría dos preguntas (¿se selecciona explorar? y ¿explorar deja que la plasticidad
  rescate?). (ii) no tiene memoria nueva, es local (lee su propia reserva) y ya sabemos que O1 usa esa lógica. La pregunta queda limpia:
  con la MISMA exploración para todos, ¿el bit plástico heredable marca la diferencia?
- El sorteo usa el rng propio del cuerpo (el de su boca) y SÓLO se consume cuando se cumplen las tres condiciones y exp = 1. Con exp = 0
  no se consume nada (arnés A1–A3), y con la puerta de reserva cerrada tampoco (arnés A4).

## 3. Instrumento y anclas
- `construye_bexp.py` (sha 62b5c174f1f3f212) → `motor_bexp.py` (0af10809633c945d): 13 anclas desde `baldwin/motor_baldwin.py`
  (d0a620d2f5e2605e), que no se toca. Instrumentación sin efecto en la simulación: contadores de mordidas exploratorias, de cuántas hicieron
  aprender a una regla plástica, de vetos, de vetos con reserva, de pasos-cuerpo y de la R de la exploración; **|w − w0| de las reglas
  plásticas de boca de CADA CUERPO QUE MUERE** (arregla el hallazgo del auditor: antes se medía sólo en los vivos en T).
- Runner `corre_bexp.py`. **Entrada (regla 14):** cada corrida ES `corre_bloques.corre` (a090b82eae9f1ee3, se importa sin tocarla) con
  el gemelo cambiado a motor_bexp. Sólo se agregan `baldwin` (las medidas de BALDWIN, mismas expresiones, + `frac_pl_fin`), `bexp`
  (exploración) y `cfg_worker` (la BQ_CFG que registró el motor). La cfg viaja en el argumento de cada trabajo (cfg por worker).
- **Arnés `identidad_bexp.py`: 40/40** (salida entera en `identidad_bexp_salida.txt`):
  - A1–A3: exp = 0 == motor_baldwin bit a bit (FIJO_V_Pinf, PLAST_V_P22k con la inversión en 22 000, PLAST_AZA_P22k), campo a campo +
    BQ_OUT salvo `cfg` y `exp`;
  - A4: exp = 1 con th_exp 2.0 (puerta cerrada: la reserva satura en 1.5) == exp = 0;
  - B: PLAST_EXP ≠ PLAST_V, FIJO_EXP ≠ FIJO_V, AZA ≠ PLAST_EXP; la exploración actúa en los 3 brazos EXP y es 0 en PLAST_V; en PLAST_EXP la
    exploración hace aprender a una regla plástica; FIJO_EXP no aprende reglas; |w − w0| se mide en los muertos;
  - G: mordidas exploratorias ≤ vetos con reserva ≤ vetos y tasa ≈ ε (|z| < 1);
  - Q: corte en 30 000 + reanuda == entera; D: determinismo; L: la letra en 12 casos sintéticos; R: banderas y candados.

## 4. Mundo, condiciones, brazos, calibración y semillas
- Mundo de BALDWIN: ECO w90, FABRICA_ECO (hijo ingenuo), MUT0 + reglas heredables (kit 1), vivero finito t_corte 100 000. VIDA = 2270.
- Inversión A↔B, C↔D cada **22 000** pasos (P/vida 9.7, el caso central) o ninguna (Pinf).
- **Brazos (6 × 20 = 120 corridas):**
  | brazo | plast | exp | papel |
  |---|---|---|---|
  | PLAST_EXP_P22k | 1 (bit heredable) | 1 | candidato |
  | FIJO_EXP_P22k | 0 | 1 | ¿basta con explorar? (control que puede ganar) |
  | PLAST_EXP_AZA_P22k | 2 (bit sorteado al nacer) | 1 | el bit sin herencia |
  | PLAST_V_P22k | 1 | 0 | referencia (= BALDWIN) |
  | PLAST_EXP_Pinf | 1 | 1 | la puerta "apaga" (secundaria) y el costo de explorar |
  | FIJO_V_Pinf | 0 | 0 | ancla de validez (= BLOQ_V) |
- **Calibración de eps_exp (regla escrita en `calibra_bexp.py`, sha 7c1e9f4b2e8e5b05, ANTES de correrla; exploración APAGADA):**
  PLAST_V_P22k en las semillas 56681 y 56682, ventana [50 000, 100 000) (diferencia de contadores de las corridas a T 50 000 y 100 000;
  la corta es prefijo exacto de la larga: comprobado). Objetivo: **4 mordidas exploratorias por vida**, porque 4 mordidas con R = +1 y
  eta_s 0.15 llevan una regla de w0 = −2.5 a ≈ −0.8, donde el hambre y el sesgo de la boca ya la dejan morder sola.
  eps = 4 / (media de las 2 semillas de vetos con reserva por vida), 2 cifras, acotado a [0.001, 0.5].
  - Resultado (`calibra_salida.txt`): s56681 **0.45** vetos con reserva por vida (ese linaje no había fijado el órgano de rechazo);
    s56682 **126.6**. Media 63.5 → **eps_exp = 0.063**.
  - **Declarado:** la media está dominada por la semilla con órgano. En un linaje con órgano fijado, 0.063 da ≈ 8 mordidas exploratorias
    por vida, el doble del objetivo; en uno sin órgano, casi ninguna. Se sigue la regla escrita; no se ajusta.
- **T = 500 000** (el de BALDWIN/BLOQUES). Costo: sec. 12.
- **Semillas NUEVAS** (grep del 29-sep: 566xx no aparece en .py/.md/.txt fuera de `datos` y `.git` en PROYECTOS/JUACO): serie
  56601–56620; réplica 56621–56640; calibración 56681–56682; arnés 56691–56694; humo 56695.

## 5. Medidas
- **persiste:** linaje vivo en T.
- **frac_pl_fin (principal para PD):** fracción plástica entre las reglas de boca que discriminan letras (píxel del foco, se cumplen en
  1–3 de las 4), en los vivos en T si los hay; si no, el último dato de `serie_pl` con ≥ 10 reglas discriminantes (el bit ANTES de
  extinguirse; la frase del encargo "sobre serie_pl antes de extinción si hace falta").
- **Exploración:** n_mord_exp, exp_por_vida, n_mord_exp_aprende, R de la exploración (+/−), vetos y vetos con reserva por vida.
- **Aprendizaje de la regla:** reglas plásticas de boca con |w − w0| > 0.05 en muertos + vivos en T (`pl_movidas`), su fracción, |w − w0|
  medio de los muertos.
- Descriptivas: K, t_ext, frac_pl en el tiempo, n_inv.

## 6. La letra (código: `lee()`)
**Validez (todas; si falla alguna: NO SE LEE):**
- V0: completa (120), sin abortos, T y t_corte correctos, bloqueados 0.
- V1: el ancla FIJO_V_Pinf persiste ≥ **13**/20 (ERR-156 H-2; antes ≥ 15, sec. 14).
- V2: cfg_worker de cada corrida = la del brazo (incluye exp, eps_exp 0.063, th_exp 0.5).
- V3: n_inv ≥ 1 en todo brazo P22k y 0 en Pinf.
- V4: la exploración actúa: n_mord_exp > 0 en ≥ 18/20 de PLAST_EXP_P22k, de FIJO_EXP_P22k y de PLAST_EXP_AZA_P22k; y = 0 en todas las de
  PLAST_V_P22k y FIJO_V_Pinf.
- V5: la regla plástica aprende POR la exploración: `pl_movidas` > 0 (muertos + vivos) **y** `n_mord_exp_aprende` > 0 en ≥ 18/20 de
  PLAST_EXP_P22k (ERR-156 H-1; sec. 14).
- V6: AZA tiene el bit al azar: mediana de `frac_pl_ult` de PLAST_EXP_AZA_P22k en [0.3, 0.7] si hay ≥ 8 semillas con dato (si no, no aplica).

**Puertas:**
- **PA rescate:** PLAST_EXP_P22k persiste ≥ 15/20 y FIJO_EXP_P22k ≤ 5/20.
- **PB control AZA:** PLAST_EXP_P22k ≥ PLAST_EXP_AZA_P22k + 5.
- **PD la selección prende:** frac_pl_fin ≥ 0.5 en ≥ 15/20 semillas de PLAST_EXP_P22k.
- **PM supera a los controles:** PLAST_EXP_P22k ≥ FIJO_EXP_P22k + 5 y ≥ PLAST_EXP_AZA_P22k + 5.

**Veredicto:** FUNCIONA = PA ∧ PB ∧ PD. HAY ALGO MODESTO = no FUNCIONA ∧ PM. NO, en otro caso.

Nota de la trampa 2: la base neutra de frac_pl es 0.5 y PD pide ≥ 0.5; lo que PD prueba es la CUENTA de semillas (con arrastre por
linaje la fracción es casi 0 o 1 por semilla). Es una puerta débil y se declara así.

## 7. Secundarias (no deciden)
- **PE "apaga"** (el encargo la nombra; la letra del director no la incluye en FUNCIONA, así que aquí no decide): frac_pl (vivos en T)
  ≤ 0.2 en ≥ 15/20 de PLAST_EXP_Pinf.
- Pareados: t_ext de PLAST_EXP contra PLAST_V, FIJO_EXP y AZA en P22k; K de PLAST_EXP_Pinf contra FIJO_V_Pinf (costo de explorar en el
  mundo estable); K de PLAST_EXP contra FIJO_EXP en P22k.
- PLAST_V_P22k (referencia): cuántas persisten (BALDWIN dio 0/20).
- R de la exploración: fracción de mordidas exploratorias con R > 0.
- **DESCRIPTIVO (ERR-156 H-4):** PLAST_EXP_P22k contra PLAST_V_P22k (persistencia, diferencia y t_ext pareado; clave
  `desc_PLAST_EXP_vs_PLAST_V_P22k`).

## 8. Regla de parada y réplica
- La réplica (56621–56640) se corre si la serie da FUNCIONA o HAY ALGO MODESTO, **o si da NO con PA, PB o PM a ±1 de su umbral**
  (ERR-156 H-3, regla 12; misma letra; NO SE LEE nunca). El bloque es el mínimo de las dos (`--bloque`).
- `--serie` y `--replica` se niegan: si el preregistro, el runner, el motor o el constructor no están commiteados y sin cambios; si ya
  hay un veredicto; si hay carpeta previa sin `--reanuda`; si otro lanzamiento tiene el candado `EN_CURSO.lock` (O_EXCL). Pool ≤ 2
  (`--pool 3` aborta; `--humo` con pool aborta). `EPS_EXP` debe estar fijado.

## 9. Predicciones (antes del humo y de la serie; se declaran refutadas si caen fuera)
| # | predicción | rango / p |
|---|---|---|
| C1 | PLAST_V_P22k persiste (repite BALDWIN) | 0–2/20 (p 0.90) |
| C2 | FIJO_EXP_P22k persiste | 2–14/20, mediana esperada ~7 (p de ≤ 5: 0.40) |
| C3 | PLAST_EXP_P22k persiste | 4–17/20, mediana esperada ~10 (p de ≥ 15: 0.20) |
| C4 | PLAST_EXP_AZA_P22k dentro de PLAST_EXP ± 4 | p 0.60 |
| C5 | FIJO_V_Pinf persiste | 12–19/20 (p de ≥ 15, V1: 0.60; BALDWIN dio 15/20 justo en el umbral) |
| C6 | PLAST_EXP_Pinf persiste menos que FIJO_V_Pinf y K pareado menor en ≥ 12/20 (explorar cuesta en el mundo estable) | p 0.65 |
| C7 | exploración: exp_por_vida mediano de PLAST_EXP_P22k | 1–15 (≈ 8 con órgano) |
| C8 | V5: pl_movidas > 0 en ≥ 18/20 de PLAST_EXP_P22k | p 0.85 |
| C9 | frac_pl_fin ≥ 0.5 en ≥ 15/20 de PLAST_EXP_P22k (PD) | p 0.30 |
| C10 | PE (secundaria) | p 0.10 |

- **Mecanismo contra H (por qué FIJO_EXP puede ganar):** tras la inversión el mundo está lleno de lo que antes se rechazaba (trampa 3).
  Con ≈ 8 mordidas exploratorias por vida, cada una de +0.8 en una reserva, el cuerpo fijo come ≈ 6.4 por vida contra ≈ 4.5 de costo
  basal: explorar solo podría bastar, sin aprender nada. Eso tumbaría PA (FIJO_EXP > 5) y es un resultado, no un fallo.
- **Mecanismo contra todos los EXP en el mundo estable:** antes de la inversión la mayoría de las mordidas exploratorias son veneno o
  sal (−0.4); ≈ 8 por vida suman ≈ 1.6 por reserva y vida contra 2.27 de costo basal (+70 %). Además, morder veneno con sed da R = 0 y
  erosiona la regla plástica de rechazo hacia 0 (el costo C7 de BALDWIN).
- **Veredicto esperado:**
  | veredicto | p |
  |---|---|
  | FUNCIONA | 0.08 |
  | HAY ALGO MODESTO | 0.17 |
  | NO | 0.45 |
  | NO SE LEE | 0.30 (sobre todo V1) |

## 10. Qué lo refuta
- H cae si PLAST_EXP_P22k no persiste ≥ 15/20 o no supera a FIJO_EXP y a AZA por ≥ 5 (PA, PB, PM).
- Si FIJO_EXP persiste como PLAST_EXP: lo que rescata es explorar (comer lo rechazado), no la plasticidad.
- Si AZA persiste como PLAST_EXP: la plasticidad ayuda, pero no su herencia/selección.
- Si V5 falla (la regla plástica no se mueve ni en los muertos): la exploración no llegó a la regla; el diseño no probó H (NO SE LEE).

## 11. Las cuatro trampas
1. **Canal simétrico:** la inversión es simétrica (A↔B, C↔D) y el bit también (inserción 0.5, flip simétrico). La exploración es
   ASIMÉTRICA a propósito: sólo prueba lo que las reglas rechazan, porque no morder no trae consecuencia (es justo el defecto que se
   repara). La señal es la del propio cerebro (R ∈ {−3, 0, +1}); no hay canal nuevo. La misma exploración se aplica a PLAST, FIJO y AZA.
2. **Acierto sin balancear:** PD tiene base 0.5 (sec. 6); V6 mide la base con AZA.
3. **Mundo que se come la comida:** tras la inversión el anillo está lleno de lo que antes no se comía (≈ 90 % B/D en los mundos con
   órgano de BALDWIN), que ahora es comida: un festín para quien cambie o para quien pruebe. Por eso FIJO_EXP es el control decisivo.
   La composición del mundo queda en el JSON (`mundo`).
4. **Sitios fijos / letras fijas:** la inversión rompe el significado fijo; la exploración es por decisión de boca, no por sitio.

## 12. Costo
Se mide en el humo (sec. 13). Proyección previa con los tiempos de BALDWIN (≈ 13 s si muere tras el vivero, ≈ 40 s si persiste a
T 500 000): peor caso 120 × 45 s / 2 ≈ 45 min con pool 2. Si el humo proyecta > 60 min, T sigue en 500 000 y se declara el costo (no se
cambia la letra).

## 13. Humo (después de escribir las secs. 1–12, sha del preregistro antes del humo 89a504ead8bdf034; semilla 56695, T 200 000, un proceso, 6 corridas; `humo_salida.txt`)
- Carpeta `datos/humo_s56695_T200000_20260929_145146/` (resumen sha 89fc1b93279b73ac). 0 abortos; validez V0–V6 pasa en modo humo;
  veredicto de humo NO (n = 1, **no cuenta**).
- **Costo (un proceso):** 12.3–14.6 s por corrida a T 200 000, mueran o persistan. Proyección de la serie a T 500 000 con pool 2: peor caso
  (todo persiste, ≈ 40 s) 120 × 40 / 2 ≈ 40 min; con la mortalidad de BALDWIN ≈ 20–25 min. Cabe en la hora. T = 500 000.
- **Números del humo (n = 1; NO cuentan):**
  | brazo | persiste | t_ext | mord. exploratorias (R+/R−) | exp/vida |
  |---|---|---|---|---|
  | PLAST_EXP_P22k | 0 | 113 872 | 87 (16/34) | 0.02 |
  | FIJO_EXP_P22k | 0 | 104 534 | 14 (0/6) | 0.003 |
  | PLAST_EXP_AZA_P22k | 0 | 107 280 | 15 (2/5) | 0.004 |
  | PLAST_V_P22k | 0 | 104 039 | 0 | 0 |
  | PLAST_EXP_Pinf | 1 (K 12.3) | — | 6 326 (4/3 237) | 1.33 |
  | FIJO_V_Pinf | 1 (K 36.7) | — | — | — |
- **Aviso, no enmienda (las predicciones de la sec. 9 NO se cambian):**
  1. En esta semilla, NINGÚN brazo P22k fijó el órgano de rechazo antes de t_corte (0 reglas discriminantes en `serie_pl` hasta 100 000):
     hay pocos vetos (0.3 con reserva por vida en PLAST_EXP), la exploración casi no actúa (0.02 por vida, lejos de las ≈ 8 de la
     calibración) y los linajes mueren de hambre y sed al acabarse el vivero (104–114 k), no por rechazar lo que ya es bueno.
  2. Esto no es nuevo: en la serie de BALDWIN, PLAST_V_P22k tenía el órgano en t_corte en 13/20 semillas (murieron tras la inversión de
     110 000) y NO lo tenía en 7/20 (murieron en 103–106 k, el colapso del vivero; `datos` de BALDWIN, leído tras el humo). **La
     hipótesis sólo puede rescatar a los linajes que tienen órgano.** Si la proporción se repite (≈ 13/20), PA (≥ 15/20) exige que la
     exploración también cambie el destino de linajes sin órgano, cosa que el mecanismo no hace. Se declara: PA es más difícil de lo
     que pensé al escribir C3; C3 y el veredicto esperado no se tocan.
  3. El costo de explorar en el mundo estable se ve grande: PLAST_EXP_Pinf K 12.3 contra FIJO_V_Pinf 36.7; 3 237 de 6 326 mordidas
     exploratorias fueron malas (R = −3) y sólo 4 buenas. En esa corrida la fracción plástica cayó a 0.0 (dirección de PE y de C6).
  4. La calibración con 2 semillas (0.45 y 126.6 vetos con reserva por vida) ya mostraba esta bimodalidad (con órgano y sin órgano).

## 14. Cambios por auditoría antes de datos (29-sep) — ERR-156
Auditor: LISTO CON CAMBIOS. Aplicados después del humo (que NO se repite) y ANTES de toda serie; sin datos nuevos. Las predicciones de la
sec. 9 NO se cambian.
- **H-1, V5 era vacua.** `pl_movidas > 0` también la pasa PLAST_V sin exploración (la regla plástica se mueve con las mordidas
  espontáneas; en el humo PLAST_V_P22k tuvo 155/204 reglas movidas). Ahora V5 = `pl_movidas` > 0 **y** `n_mord_exp_aprende` > 0 (al
  menos una mordida exploratoria hizo aprender a una regla plástica) en ≥ 18/20 de PLAST_EXP_P22k.
- **H-2, V1 = FIJO_V_Pinf ≥ 13/20** (decisión del coordinador). Motivo: con p ≈ 0.75–0.8 de persistir y n = 20, ≥ 15 falla con
  probabilidad ≈ 0.2–0.4 aunque el ancla esté sana, y la única calibración previa, BALDWIN, dio 15/20, justo en el umbral. Con ≥ 13 la
  falla de un ancla sana baja a ≈ 0.02–0.10. **Declarado:** mi p 0.30 de NO SE LEE (sec. 9), que venía casi toda de V1, queda alta con
  la letra nueva; no la cambio.
- **H-3, regla 12:** si PA, PB o PM quedan a ±1 de su umbral, la réplica se corre con la misma letra aunque el veredicto sea NO.
  Definición en código (`cerca_umbral`): PA si |PLAST_EXP − 15| ≤ 1 o |FIJO_EXP − 5| ≤ 1; PB si |PLAST_EXP − (AZA + 5)| ≤ 1; PM si
  |PLAST_EXP − (FIJO_EXP + 5)| ≤ 1 o |PLAST_EXP − (AZA + 5)| ≤ 1. `replica_permitida()` lo aplica en `--replica`; NO SE LEE no replica
  nunca. El resumen guarda `cerca_umbral`.
- **H-4, declarado:** PM no exige piso (un PLAST_EXP 6/20 con FIJO_EXP 1 y AZA 1 da MODESTO) y no se compara con PLAST_V_P22k. No se
  cambia la letra de PM; se añade como DESCRIPTIVO PLAST_EXP_P22k contra PLAST_V_P22k (sec. 7).
- **H-6, arnés rehecho entero con el runner final: 52/52** (`identidad_bexp_salida.txt`, sha b09b4d75e8a735bc; `identidad_bexp.py`
  54830365330392a2; `corre_bexp.py` fdc5e729057e7bd8; motor y constructor sin cambios: 0af10809633c945d, 62b5c174f1f3f212). Casos
  sintéticos nuevos de la letra:
  - H-1: la regla se mueve pero no por la exploración → NO SE LEE;
  - H-2: ancla 13/20 → FUNCIONA; 12/20 → NO SE LEE;
  - H-3: NO con PM a 1 → réplica permitida; NO lejos → no; NO SE LEE cerca → no; FUNCIONA y MODESTO → sí;
  - H-4: el descriptivo está presente.
- El humo de la sec. 13 se corrió con el runner anterior (8ef1d0da7feeb333), que difiere del final sólo en la letra (V1, V5, réplica y
  descriptivo); la simulación y las medidas por corrida son las mismas.
