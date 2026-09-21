# PREREGISTRO — **dE5 bajo el CRITERIO DE TRONCO v2** (siete puertas, semillas NUEVAS 2001–2080)

Creador, 21-sep-2026. Ejecuta `registro/CRITERIO_TRONCO_v2.md` sobre **dE5 = v14.2 + la SORPRESA DEL MUNDO en la
BOCA a dosis k = 5**. Decisión del director (18-sep, ratificada 21-sep): dE5 se corre después de v15f; v15f ya se
corrió y NO ENTRA (cayó T-A, T-C, T-D, T-E). **§1–§6 escritos ANTES de mirar un solo número del candidato; §7 (humo)
después, y se dice.** Sin `Pool` por mi parte, sin commits, nada congelado tocado, ningún proceso ajeno tocado.

**Misión (primero):** llegar a la AGI por este camino — un organismo que **generaliza, se desdice y vive**. Lo que
dE5 aporta a esa escalera no es una capacidad de cálculo: es **volver a probar cuando el mundo deja de comportarse
como el organismo predice**, con una señal que el organismo ya fabrica (el error de su propio predictor de ΔE) y sin
una sola constante nueva ni un byte de memoria nueva. Es el peldaño 9 (autonomía) entrando por la puerta de la
conducta, no por la del diseño.

---

## 1. Lo que YA está medido de este mecanismo (no se rejuzga; es la base de la predicción)

`PREREGISTRO_probar_si_mismo.md` y `PREREGISTRO_dosis_dE.md`, brazos `dE-TEST` / `dE5`, sobre **v13**:

| medida | k = 10 (descartada) | **k = 5 (esta dosis)** |
|---|---|---|
| recuperación tras el cambio no avisado (× V13) | 0.143 / 0.144 / 0.141 (41–100) | **0.267 (121–140) y 0.248 (141–160)** |
| pareado (recupera antes que V13) | 20/20 ×3 | **20/20 ×2** |
| se apaga sola (P4′ relativo) | 20/20 ×3 | **20/20** |
| G1 valor (px0) | **0.750 — FALLA el 0.80** | **0.800** |
| G2 conducta | 0.870 | 0.857 |
| K cobertura | 20/20 | 20/20 |
| examen v3″ retención | 8/8 | **8/8** |

Todo eso está medido **sobre v13** y **bajo el criterio v1**. Aquí se vuelve a medir todo **sobre v14.2** (que trae
hija dispersa, puerta por código y B-5) y **bajo el criterio v2**, con **semillas nuevas**. Nada de lo de arriba
cuenta como puerta: cuenta como predicción.

---

## 2. Instrumentos (por anclas; ningún congelado tocado; `manifiesto.py` verifica 20/20 antes y después)

Constructor único: **`construye_v15_dE5.py`**. Orígenes, con sha fijado como tripwire (si uno cambia, no se escribe
nada):

| archivo generado | origen (SÓLO se lee) | sha origen |
|---|---|---|
| `organismo_v15_dE5.py` | `experimentos/nivel11_mundo_vivo/organismo_vivo_rep2.py` | `96feb4918dc5d694` |
| `organismo_v15_dE5_on.py` | el anterior, con la dosis por defecto | — |
| `organismo_v15_dE5g.py` / `_on.py` | `organismo/organismo_v142g.py` | `9e5f566cd6a7a4d2` |
| `bateria_v15_dE5.py` | `organismo/bateria_v142.py` **(CONGELADA)** | `6375d90e531b06e6` |
| `bateria_generaliza_v15_dE5.py` | `organismo/bateria_generaliza_v142.py` **(CONGELADA)** | `e5929942647756a5` |
| (referencias) | `organismo/organismo_v142.py` `17528d767fcebaf6`, `organismo_vivo.py` `20c0961c79de8825`, `organismo_v14.py` `feefc88b1fd8d434` | |

**Por qué el origen es `organismo_vivo_rep2` y no `organismo_v142`, si el candidato es v14.2 + dE.** Porque las
puertas T-A (r = descendientes − muertes), T-C (ii) y T-D viven en el **mundo vivo**, y ese mundo es `organismo_vivo`
← v14.1; `rep2` le añade las perillas de reproducción que T-A necesita. La cadena `rep2` es v14.**1**, así que **B-5
no está dentro**: por eso el constructor le añade B-5 **con el texto literal** de
`experimentos/creacion_B/construye_codigo.py` (`COND_A`→`COND_B` y `FIS_VA`→`FIS_VB`, el mismo código que pasó
`identidad_codigo.py` y las dos series de B-5), con **`desambiguar=1` por defecto, como el tronco v14.2**. El arnés
comprueba que la cadena entera cierra: con `vivo=0, n_nec=1` y la dosis apagada, el candidato es
`organismo/organismo_v142.py` **bit a bit**.

**El mecanismo dE NO se escribe aquí: ya estaba.** `organismo_vivo_rep2` trae el predictor de ΔE del bloque 6
(`eta_pred`, `ema_pred`, `clip_e`) y su entrada en la boca (`k_sorp`), vectorial por necesidad. Con `n_nec = 1` es,
operación por operación, el `dE-TEST` de `organismo_v13E_k5`:

```
_dp  = Wpe@P + Wke@kenyon(P)                       (predictor lineal de ΔE, al morder)
_ep  = ΔS_real − _dp        (con n_nec=1, ΔS_real = E_VAL[valencia])
Wpe <- clip(Wpe + eta_pred·outer(_ep,P),        ±clip_e)
Wke <- clip(Wke + eta_pred·outer(_ep,kenyon(P)),±clip_e)
_sbE<- (1−ema_pred)·_sbE + ema_pred·|_ep|          (CAUSAL: la usa la boca del PRÓXIMO encuentro)
Vb   = alpha·w + hambre_boca·hambre + 0.5 + k_sorp·_sbE
```

**dE5 = `eta_pred=0.03, ema_pred=0.05, clip_e=3.0, k_sorp=5.0`.** Ni una constante más. **Memoria nueva: CERO**
(`Wpe`, `Wke`, `_sbE` ya existían en el instrumento del mundo vivo; en v14.2 son 6 + 90 + 1 números).

**Lo único que el constructor añade además de B-5, y por qué:**
1. `invertir_vivo_en` (T-C ii): en `t` se intercambian los EFECTOS de comida y veneno. Texto idéntico al de
   `experimentos/creacion_A/construye_vivo_relevo.py`. Inerte por defecto (`None`).
2. Lecturas de SOLO LECTURA para T-G: `t_ext_B` (primer paso tras `invertir_en` con `valor(B) ≥ 0` — el M1 del
   bloque 6, el mismo de C-P1), `mord_post`, `deaths_post`, `sbarE`, `sesgo_q` (el sesgo medio de la boca por cuarto:
   es lo que mide **si se apaga solo**) y `enc_q`. Ninguna consume rng.
3. `sesgo_fijo` (perilla **del control**, 0 por defecto): un empujón constante en la boca. Es el brazo `CONST` de
   C-P1 trasplantado: **misma cantidad de empuje, sin información**. El candidato nunca lo usa.

**Regla 14 — entrada nueva de la batería copiada, campo a campo contra la del tronco.** La entrada del tronco en
`organismo/bateria_generaliza_v142.py` es

```
'organismo_v142': ('organismo_v142g', dict(eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25,
                                           del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1))
```

y las dos entradas nuevas llevan **los mismos diez campos, con los mismos valores**, más las **cinco perillas
restantes EXPLÍCITAS** (ERR-38: "por defecto" no existe cuando el módulo es otro):

```
'organismo_v15_dE5_on': ('organismo_v15_dE5g_on', dict(<los DIEZ campos, idénticos>,
                          desambiguar=1, eta_pred=0.03, ema_pred=0.05, clip_e=3.0, k_sorp=5.0))
'organismo_v15_dE5'   : ('organismo_v15_dE5g',    dict(<los DIEZ campos, idénticos>,
                          desambiguar=1, eta_pred=0.0,  ema_pred=0.05, clip_e=3.0, k_sorp=0.0))
```

(la entrada del tronco no pasa `desambiguar` porque el defecto del módulo ya es 1: **mismo valor**, escrito
explícito aquí). Comparación campo a campo en §8. Las dos baterías copiadas pasan un **humo que escribe su JSON**
antes de la serie (ERR-42).

**Arnés `identidad_v15_dE5.py` — 61 identidades + 7 controles que DEBEN fallar.**
Identidades: **I1** candidato(`vivo=0, n_nec=1`, dosis OFF) == `organismo_v142` en TODAS sus claves, 9 escenarios ×
3 semillas · **I2** candidato(`desambiguar=0`, dosis OFF) == `organismo_vivo_rep2`, 4 montajes × 2 semillas (VIVO,
CUELLO_MIN, BASE del bloque de la sal, VIVO de mini_vivo) · **I3** el módulo de mundo de regla == `organismo_v142g`
(px0, azar, AB) con los kwargs EXACTOS de INSTRUMENTOS · **I4** B-5 inerte en los mundos del tronco
(`desambiguar=1` == `0`) · **I5** el predictor SÓLO MIDE (`eta_pred=0.03, k_sorp=0`) == apagado del todo · **I6**
las DOS implementaciones del dE coinciden (el módulo de mundo de regla en `mundo='AB'` con la dosis ON ==
el del mundo vivo con `n_nec=1` y la dosis ON) · **I7** `invertir_vivo_en > T` es inerte.
Controles que deben fallar: **M1** dosis ON ≠ OFF · **M2** dosis 10 ≠ dosis 5 · **M3** `desambiguar=1` ≠ `0` en una
semilla ALIAS · **M4** `invertir_vivo_en = T/2` sí cambia · **M5** paja del comparador (semillas distintas) · **M6**
en el mundo de regla la dosis ON ≠ OFF · **M7** `sesgo_fijo` sí empuja la boca.
**Si el arnés no sale N/N, el runner se para y no hay veredicto.**

---

## 3. Semillas NUEVAS (verificadas con `grep` contra todo el repo: `.py`, `.md` y `datos/`)

**`141–160` NO están libres**: las usó el examen v3′ de v14 y la réplica de recuperación de dE5 sobre v13
(`PREREGISTRO_dosis_dE.md`, enmienda 1). Tampoco `161–200`, `201–340`, `401–760`, `821–960`, `1201–1230` ni
`1000–1999` (pool de réplica de `externo_mundo_minimo`). Se usan por primera vez en el proyecto:

| puerta | semillas | instrumento |
|---|---|---|
| T-B, T-C (i), T-E, T-F (examen) | **2001–2020** | `bateria_generaliza_v15_dE5.py` y `bateria_v15_dE5.py` |
| T-A supervivencia | **2021–2040** | `corre_vivo_rep2.BRAZOS` VIVO y CUELLO_MIN |
| T-C (ii) reversión en el mundo vivo | **2041–2060** | `mini_vivo.BRAZOS['VIVO']` + `invertir_vivo_en = 50 000` |
| T-G capacidad nueva (recuperación) | **2061–2080** | mundo AB del tronco, `T = 200 000`, `invertir_en = 100 000` |
| T-D | las 9 ALIAS y 9 LIMPIAS de `corre_sal` (estructurales, no elegibles) | `corre_sal.BASE`, sal muda |

---

## 4. Las SIETE puertas (la letra copiada de `CRITERIO_TRONCO_v2.md`; instrumento y semillas por puerta)

| puerta | instrumento | semillas | umbral (letra de v2) |
|---|---|---|---|
| **T-A sobrevive** | `corre_vivo_rep2` brazos **VIVO** y **CUELLO_MIN**, dosis ON y OFF, pareado por semilla (`T=100 000`, `costo=0.001`) | 2021–2040 | muertes ≤ **1.10 ×** tronco (mediana); r = descendientes − muertes ≥ tronco − **10**; **A₁₂(r) ≥ 0.50** |
| **T-B generaliza** | `bateria_generaliza_v15_dE5.py organismo_v15_dE5_on 20 --desde 2001 --log` | 2001–2020 | **G1 ≥ 0.80, G2 ≥ 0.85**, azar ∈ [0.35, 0.65] (G2 azar ∈ [0.42, 0.58]), **K 20/20** |
| **T-C se desdice** | (i) examen E2 leído por CONDUCTA: "come B Q4 ≥ 50" · (ii) mundo vivo con `invertir_vivo_en = 50 000`, ON/OFF pareado | (i) 2001–2020 · (ii) 2041–2060 | (i) **≥ 18/20** · (ii) **A₁₂(ON > OFF) ≥ 0.75** en `rev = mord[B][Q4] − mord[A][Q4]` |
| **T-D sin alias** | bloque de la sal (`corre_sal.BASE`, sal muda), 9 ALIAS + 9 LIMPIAS, ON/OFF | las del bloque | **C1, C2, C6** de B-5, **importados** de `creacion_B/corre_codigo.UMBRALES` (no copiados) |
| **T-E no regresión conductual** | examen del candidato contra el del **tronco v14.2** (`bateria_v142.py 20 --desde 2001`), pareado por semilla | 2001–2020 | por escenario **≥ 18/20** (cláusulas en §5) |
| **T-F coste** | examen: celdas, divisiones, muertes (medianas de las seis etapas); mundo vivo: con T-A | 2001–2020; 2021–2040 | **≤ 1.25 ×** tronco |
| **T-G capacidad nueva** | recuperación tras el cambio no avisado: mundo AB del tronco, `T = 200 000`, `invertir_en = 100 000`, brazos OFF / **dE5** / **CONST** / dE10 | 2061–2080 | ver §6 |

**Regla de cierre (regla 2 del criterio v2): una sola puerta caída → NO ENTRA, sin modos intermedios.**

---

## 5. T-E: la conducta por escenario, definida ahora (letra copiada de `PREREGISTRO_v15f_v2.md` §4)

Pareado por semilla contra **v14.2** en 2001–2020; una semilla cuenta si cumple TODAS las cláusulas de su escenario;
puerta = **≥ 18/20** por escenario. Tolerancias **1.10** (conteos) y **0.8** (lo que debe comer). Los pesos internos
(W_B ≈ −3, etc.) se **REPORTAN**, no son puerta.

- **E1:** (a) mordidas totales de veneno (B, Q1–Q4) ≤ 1.10 × tronco; (b) comida comida en Q4 ≥ 0.8 × tronco.
- **E2:** (a) come B Q4 ≥ 50 (es T-C i); (b) muerde A en Q4 ≤ 1.10 × tronco.
- **E2I:** (a) mordidas totales de C ≤ 1.10 × tronco; (b) `tasaA Q4 ≥ 80 % Q2`.
- **E2J / E2K:** (a) come D en Q4 ≥ 0.8 × tronco; (b) mordidas totales de B ≤ 1.10 × tronco.
- **E2L:** (a) mordidas totales de B ≤ 1.10 × tronco; (b) come A en Q4 ≥ 0.8 × tronco.

**Aviso escrito antes de correr:** E1(a) es el subcriterio que más directamente castiga a este mecanismo — la
sorpresa *empuja a morder*, y lo que se cuenta es veneno mordido. Si dE5 cae, lo más probable es que caiga aquí.

---

## 6. T-G: la capacidad nueva, su umbral y sus controles

**Capacidad declarada: "recuperarse de un cambio no avisado 4–7 × más rápido que el tronco, sin envenenarse más, y
apagando sola las ganas de probar cuando el mundo vuelve a ser predecible."** No es XOR ni nada que el tronco ya
haga peor: es una conducta que v14.2 **no tiene**.

Medida: `recup = t_ext_B − invertir_en`, censurada a `T − invertir_en = 100 000` si nunca ocurre (`t_ext_B` = primer
paso tras la inversión en que `valor(B) ≥ 0`; el M1 del bloque 6, sin cambiar una coma).

**Umbrales — COPIADOS de `PREREGISTRO_dosis_dE.md` §6, no inventados aquí** (condiciones 1, 2 y 3), más un control
de cantidad nuevo:

| # | condición | umbral |
|---|---|---|
| G-1 | recuperación mediana dE5 / mediana OFF | **≤ 0.60 ×** |
| G-2 | pareado (dE5 recupera antes que OFF, misma semilla) | **≥ 16/20** |
| G-3 | **se apaga sola** (P4′ relativo sobre `sesgo_q`): Q2 ≤ 0.10, Q4 ≤ 0.10, Q2 ≤ 0.35·Q3, Q4 ≤ 0.35·Q3 | **≥ 16/20** |
| G-4 | **control de CANTIDAD**: el brazo `CONST` (`sesgo_fijo = C`, mismo empujón medio, sin información) NO recupera como dE5: razón(CONST) > razón(dE5) y pareado (dE5 < CONST) | **≥ 15/20** |
| G-5 | no se envenena más: mordidas de veneno tras la inversión (`mord_post`) ≤ **1.10 ×** OFF (mediana) | — |

`C` (la ganancia del control de cantidad) se fija en el **humo**, §7, como la mediana del sesgo de la boca de dE5
tras la inversión, y **queda escrita ahí antes de la serie**: es el único número que el humo fija (mismo
procedimiento que los brazos `CONST-a`/`CONST-b` de C-P1, cuyos 0.173 y 0.31 salieron de una medición previa).
El brazo `dE10` corre como **referencia** (dosis ya descartada por G1), sin umbral.

---

## 7. Predicción numérica, firmada ANTES del humo y de la serie

| puerta | predicción (rango) | ¿pasa? |
|---|---|---|
| **T-A** | muertes ON/OFF **0.90–1.05 ×**; r_ON − r_OFF **−5 a +10**; A₁₂(r) **0.50–0.70** | **SÍ**, ajustado |
| **T-B** | G1 **0.95–1.00** (base v14.2 = 1.000; el coste medido a dosis 10 fue −0.05, a dosis 5 fue 0.00), G2 **0.90–1.00**, azar 0.40–0.60, K 20/20 | **SÍ** |
| **T-C (i)** | come B Q4 ≥ 50 en **19–20/20** | **SÍ** |
| **T-C (ii)** | A₁₂(rev ON > OFF) **0.60–0.85** | **INCIERTO** — la reversión del mundo vivo cambia EFECTOS, no la regla de la retina; es la segunda candidata a caer |
| **T-D** | C1 ≥ 8/9 con mediana \|W[sal]\| ≤ 0.1 (B-5 dentro), C2 ≥ 8/9 y ≤ −2.5 9/9, C6 9/9; exposiciones a la sal ≤ **1.2 ×** OFF | **SÍ** |
| **T-E** | E2/E2J/E2K/E2L **19–20/20**; E2I **18–20/20**; **E1 17–20/20** (el filo: veneno total ≤ 1.10 ×) | **SÍ** con riesgo real en E1 |
| **T-F** | celdas **1.00–1.10 ×**, splits **1.00–1.20 ×**, muertes **0.95–1.10 ×** | **SÍ** |
| **T-G** | razón **0.14–0.30** (4–7 ×; sobre v13 fue 0.267 y 0.248), pareado **17–20/20**, apagado **18–20/20**, CONST razón **0.70–1.00** | **SÍ** |

**Veredicto esperado:** dE5 cruza las siete con probabilidad que declaro **~40 %**; las caídas más probables, en
orden: **T-E (E1, veneno total)**, **T-C (ii)**, **T-A**. Si cae una sola, NO ENTRA.

**Números que firmo y que pueden quedar refutados aunque la puerta pase:**
1. "4–7 × más rápida": si la razón cae en (0.30, 0.60] la puerta G-1 pasa pero **la capacidad declarada queda
   refutada** y se registra así, con letras, en el informe y en el registro. No se recalibra el titular después.
2. "sin coste de generalización sobre v14.2": si G1 ∈ [0.80, 0.95) la puerta pasa pero la predicción de "coste 0"
   queda refutada.
3. "B-5 protege el alias también con la sorpresa encendida": si T-D pasa en el brazo OFF y cae en dE5, el mecanismo
   **rompe una reparación ya declarada** y eso es un resultado, no un ruido.

**Qué lo refuta por completo:** cualquier puerta por debajo de su umbral. Y, específicamente para la hipótesis de
fondo — *la sorpresa del mundo en la boca es un órgano y no un empujón* —: que el brazo **CONST** (G-4) recupere
igual o más rápido que dE5. Si eso pasa, lo que acelera la recuperación es **la cantidad de empuje**, no la
información del predictor, y el mecanismo se cierra aquí (y las tres series de C-P1 quedan reinterpretadas).

---

## 8. Regla 14 — entrada campo a campo, y cláusulas

Se escribe en el informe la tabla de los diez campos del tronco contra los diez del candidato, valor a valor.
`mem_*` no existe aquí. `invertir_vivo_en = 50 000` para T-C (ii) y la dosis
(`eta_pred=0.03, ema_pred=0.05, clip_e=3.0, k_sorp=5.0`) quedan **fijados aquí**. Ningún umbral se mueve tras ver
datos; si hiciera falta moverlo, ERR numerado (libres desde **ERR-90**), criterio nuevo y semillas nuevas. Réplica
en semillas nuevas antes de congelar (regla 2 del criterio v2); la decisión de tronco es del director.

**Prueba de un proceso (humo), lo que está permitido:** ≤ 6 corridas, ≤ 200 000 pasos, sin `Pool`. Las semillas del
humo son **2061 (T-G), 2021 (T-A) y una ALIAS (T-D)**, declaradas aquí: se miran a sabiendas y **ningún umbral se
toca después de verlas**.

---

## 9. Cómo se corre

```
python experimentos/tronco_v15_dE5/construye_v15_dE5.py          # reconstruye los 6 archivos (idempotente)
python experimentos/tronco_v15_dE5/identidad_v15_dE5.py 20000    # arnes: N/N o no hay veredicto
python experimentos/tronco_v15_dE5/corre_dE5_v2.py --humo        # UN proceso, sin Pool, escribe su JSON
JUACO_POOL=14 python experimentos/tronco_v15_dE5/corre_dE5_v2.py # las nueve etapas (lo corre el COORDINADOR)
python experimentos/tronco_v15_dE5/corre_dE5_v2.py --solo TA,TG  # subconjunto de etapas
```

---

## §10 — HUMO (medido DESPUÉS de §1–§9; UN proceso, sin `Pool`, 6 corridas)

`datos/humo/dE5_v2_humo_20260921_150430.log` / `.json` (`858cc687d32e583f`), script `corre_dE5_v2.py`
`c042de285398a333` (repetido tras fijar `C_CONST`; la corrida previa `..._145417` / `4f5e1f08c2bd5d6b`
con el sha anterior da los MISMOS numeros). Arnés
`identidad_v15_dE5.py`, instrumento `organismo_v15_dE5.py` `7e2c9aed98047fee` / `_on` `00aaa9563c30247b`.

**(a) Identidad: ARNÉS TOTAL 68/68** — 61/61 identidades (con la dosis apagada y `vivo=0, n_nec=1` el candidato es
`organismo_v142` **bit a bit** en los 9 escenarios × 3 semillas; con `desambiguar=0` es `organismo_vivo_rep2` bit a
bit en los 4 montajes; el módulo de mundo de regla es `organismo_v142g` bit a bit; B-5 inerte en los mundos del
tronco; el predictor que sólo mide es idéntico al apagado; **las dos implementaciones del dE coinciden bit a bit**)
y **7/7 controles que fallan como deben**.

| etapa | semilla | OFF (= v14.2) | dE5 (k_sorp = 5) |
|---|---|---|---|
| **T-G** recuperación (T = 200 000, `invertir_en` = 100 000) | 2061 | recup **4 356** (t_ext_B 104 356), veneno tras el cambio 54, muertes 263/126, `sesgo_q` [0, 0, 0, 0] | recup **1 097** (t_ext_B 101 097), veneno tras el cambio **51**, muertes 263/**117**, `sesgo_q` **[0.103, 0.0001, 0.115, 0.0002]** |
| **T-A** mundo vivo rep2, brazo VIVO | 2021 | r **−64** (desc 25, muertes 89 [49, 40]), celdas 30, splits 0 | r **−88** (desc 18, muertes **106** [54, 52]), celdas 30, splits 0 |
| **T-D** bloque de la sal, ALIAS, sal muda | 326 | \|W[sal]\| **0.0**, W[veneno] **−3.0**, exp sal 556, des_splits 6, muertes 38 | \|W[sal]\| **0.0**, W[veneno] **−3.0**, exp sal 546, des_splits 5, muertes 33 |

**Razón dE5/OFF en la 2061: 0.252 (4.0 × más rápido).** El humo **no es la puerta**: 2061, 2021 y 326 son una
semilla de cada bloque, están declaradas en §8 y **ningún umbral se toca después de verlas**.

**El único número que el humo FIJA (§6, G-4): `C = 0.058`** = media de `sesgo_q` en Q3–Q4 de dE5 en la 2061
(0.114829 y 0.000238). El brazo `CONST` de la serie aplica ese empujón constante. Escrito en `corre_dE5_v2.py`
(`C_CONST = 0.058`, sobreescribible con `JUACO_CONST`). Es el **único** cambio de código entre las dos corridas del humo.

**Lo que el humo dice contra mis predicciones, escrito aquí sin cambiar §7:**
1. **T-A va peor de lo que predije** en la única semilla mirada: muertes 106 contra 89 = **1.19 ×**, por encima del
   1.10 de la puerta, y r cae 24. Mi predicción de §7 ("muertes 0.90–1.05 ×, A₁₂(r) 0.50–0.70, PASA ajustado") queda
   **en riesgo serio**; si la serie lo confirma, esa predicción queda refutada y dE5 cae por T-A. No la reescribo.
2. **La forma de `sesgo_q` es la firma del mecanismo**, y es mejor de lo que pedía la letra: sube al aprender
   (Q1 0.103), se apaga (Q2 0.0001), **vuelve a subir sola cuando el mundo cambia** (Q3 0.115) y se apaga otra vez
   (Q4 0.0002). Es "se apaga sola" **dos veces** en la misma corrida.
3. **T-D limpio con la dosis encendida**: B-5 sigue reparando el alias (|W[sal]| 0.0, veneno −3.0) y `des_splits`
   sigue disparándose (5). La sorpresa no rompe la reparación en esta semilla.

**Humo de las baterías copiadas (ERR-42), aparte y también sin `Pool`:**
- `bateria_generaliza_v15_dE5.py organismo_v15_dE5_on 1 --desde 2001 --log --sin-pool` **llegó a escribir su JSON**
  (`datos/regresion_generaliza_dE5_organismo_v15_dE5_on_20260921_144112.json`, `dcfea62dc85e35ad`): G1 1.000,
  G2 0.998, azar 0.500 / 0.421, K 1/1 en la semilla 2001 (una semilla, **no es la puerta**).
- `humo_bateria_examen.py` (3 corridas, sin `Pool`): **7/7**. El humo completo de `bateria_v15_dE5.py` no lo puede
  correr un agente (su criterio 5 son 168 corridas antes del examen); su ruta de escritura se probó de verdad
  creando y borrando un archivo en `datos/` con el mismo prefijo.

**ERRORES QUE EL HUMO CAZÓ (los dos, en mi propio código, antes de la serie):**
- **ERR-30 repetido.** La batería del examen copiada reducía a v11/v10 con `eta_s=0, puerta=None` pero **dejaba la
  dosis encendida** (el módulo examinado la trae ON por defecto): el criterio 5 daba `identico=False` y el examen
  entero se habría abortado. Corregido en el constructor pasando `eta_pred=0, k_sorp=0, sesgo_fijo=0` EXPLÍCITOS.
- **ERR-42 repetido, en mi runner.** El `--humo` escribía su JSON en una variable de ruta que no existía: reventó
  **después** de imprimir los seis resultados y perdió el JSON. Corregido y vuelto a correr entero.
