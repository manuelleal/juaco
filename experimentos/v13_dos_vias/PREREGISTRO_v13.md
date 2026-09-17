# v13 — DOS VÍAS: ¿rompe el canje entre recordar y generalizar?

**Escrito ANTES de construir y de correr. 17 sep 2026, día 5.** Dirección: *"córrelo… explorar, avanzar más que
frenar, siguiendo el método"*.

## 0. De dónde sale

- El canje está medido (`v12_superficie_20260917_154123`): ninguna perilla **dentro de una sola vía** logra a la vez
  retención 20/20 y acierto ≥ 0.78 en patrones nunca vistos; la hija que madura tampoco (congelar lo justo para no
  olvidar es congelar demasiado para aprender).
- La literatura (McClelland, McNaughton y O'Reilly, 1995) y nuestros datos apuntan a lo mismo: no una perilla, sino
  **dos sistemas** —uno rápido y separado que recuerde, otro lento y distribuido que generalice— que comparten el
  error.

## 1. Mecanismo (v13 = v11 + vía lenta)

- **Vía rápida:** v11 sin tocar (Kenyon, división por conflicto de signo, hija ciega, madre fija, fisión).
- **Vía lenta:** una lectura **lineal directa de la retina** (6 píxeles), con dos canales `Wp_s`, `Wn_s` ∈ ℝ⁶ (≥ 0,
  tope 3), tasa `eta_s` **menor** que la de la rápida, mismo drenaje de la parte común. Es la representación **más
  solapada posible** (cada píxel lo comparten muchos patrones): por construcción interfiere y por construcción
  generaliza. Es la "corteza" del esquema CLS en su forma mínima.
- **Un solo error para las dos:** `valor(P) = (Wp − Wn)·kenyon(P) + (Wp_s − Wn_s)·P`; `dlt = R − valor`. La rápida y
  la lenta se actualizan con el **mismo** `dlt`, cada una a su tasa. La boca decide con `valor`. Ninguna vía "enseña" a
  la otra: se reparten el error como en un residual.
- **Con `eta_s = 0` la vía lenta es inerte (pesos en cero) y v13 es v11 EXACTO.** Es el control de inercia.

## 2. Instrumentos

`organismo_v13.py` desde `organismo_v11.py` (`f69e24063be1b194`) por anclas; `v13m` (bloque M) y `v13g` (mundo de
regla) con las anclas de siempre, donde toda lectura de valor (`W`, sondas, `W_apriori`, primer encuentro) pasa a ser
el `valor` total que usa la boca. Identidades obligatorias (si fallan, se para): `v13(eta_s=0)` ≡ v11 (7 escenarios ×
1–3); `v13m(eta_s=0)` ≡ `v11m`; `v13g(eta_s=0)` ≡ `v11g`.

## 3. Diseño

Superficie de la tasa lenta, **todos los puntos se reportan**: `eta_s ∈ {0 (= v11), 0.003, 0.006, 0.015, 0.03}`
(la rápida usa `eta = 0.03`). Semillas **41–60** para la superficie (exploración declarada).

Medidas (todas ya preregistradas en sus experimentos): retención del bloque M (`W_B ≤ −2` y `W_A ≥ 0.5`) con su
guarda; acierto en patrones nunca vistos (`px0`), control `azar`, frontera `xor01`; conducta al primer encuentro;
y **las tres etapas del examen más sensibles** (E1, E2, E2L) con sus criterios exactos del criterio v3, para no
comprar generalización a costa de aprender, revertir o separar.

**Confirmatorio dentro de la misma corrida, y separado del barrido:** si algún `eta_s` cumple en 41–60 retención
≥ 18/20 **y** acierto ≥ 0.78, **ese único punto** se vuelve a correr en semillas **61–80** (nunca usadas para esto) y
**sólo el resultado en 61–80 decide**.

## 4. Predicciones (escritas antes)

- **P1 [inercia]:** identidades 100 %.
- **P2 [la lenta generaliza lo lineal]:** con `eta_s ≥ 0.006`, acierto `px0` ≥ **0.80**; `azar` en [0.35, 0.65];
  `xor01` ≤ 0.60 (una lectura lineal **no puede** resolver XOR: si sube, algo está mal).
- **P3 [la rápida sigue recordando]:** con `eta_s ≤ 0.006`, retención ≥ **18/20** y guarda ≥ 18/20. Riesgo declarado:
  la vía lenta **se lleva parte del valor** de B y luego **deriva** mientras B no está (comparte píxeles con C y D);
  si esa deriva pasa de ~1 unidad, `W_B` sube por encima de −2 y P3 cae.
- **P4 [el canje se rompe]:** existe al menos un `eta_s` con retención ≥ 18/20 **y** acierto ≥ 0.78 en 41–60, **y se
  sostiene en 61–80**. *Predicción: sí, en `eta_s = 0.006` o `0.003`.*
- **P5 [nada se rompe]:** E1, E2 y E2L ≥ 18/20 en ese punto.
- **Refutación de la idea:** ningún `eta_s` logra P4, o lo logra en 41–60 y cae en 61–80 (sobreajuste), o lo logra
  rompiendo P5.

## 5. Qué se decide

- **P4 y P5 en 61–80:** v13 pasa a **candidato a tronco** y se lleva al confirmatorio completo (examen criterio v3 en 20
  semillas nuevas, `bateria_generaliza.py 20`, re-verificación 3T). Se escribe: *"dos vías con un solo error rompen el
  canje en este sistema"*, y se anota que la lenta es lineal (generaliza lo lineal, no XOR).
- **P4 falla:** se registra la superficie completa, v11 sigue de tronco, y **se pasa a la Etapa 5 con v11** y la
  limitación declarada (decisión ya tomada con dirección).
- **Falla P1:** se para y se arregla el instrumento.

## 6. Qué NO prueba

No prueba que la lectura lineal sea "la" corteza: es la vía lenta más simple posible. No prueba generalización no
lineal (XOR seguirá fallando, y así se predice). No prueba nada sobre 3T ni sobre capacidad, que se re-verifican si
v13 pasa a candidato.

---

## ENMIENDA 1 (17 sep, tras el humo de instrumentos y ANTES de correr) — dos brazos, no uno

**Humo declarado (semilla 41, una corrida por punto; 41 está en el conjunto de la superficie, se declara):**
1. Identidades P1: `v13(eta_s=0)` ≡ v11, `v13m` ≡ `v11m`, `v13g` ≡ `v11g`: idénticos.
2. **Con un solo error compartido, la vía rápida deja sin error a la lenta** (aprendizaje residual): en el bloque M la
   lenta sólo captura −0.42 de −3 en B con `eta_s = 0.006` y −1.02 con `0.03`; en el mundo de regla el acierto a
   priori queda en 0.50–0.60. **La predicción P2 tal como estaba escrita probablemente falla por esa razón**, que es
   de diseño y no de medida. Se mantiene el brazo (es lo preregistrado) y se añade otro.
3. **Brazo nuevo, `puerta`:** cada vía aprende de **su propio** error (`dlt_f = R − rápida`, `dlt_s = R − lenta`) y
   la boca **consulta** una u otra: la rápida cuando el patrón le es **familiar**, la lenta cuando no. Primer intento,
   puerta por magnitud (`|rápida| ≥ 0.5`): retiene (W_B −2.93, W_A +1.05) y revierte (E2: come B 82 en Q4), pero el
   acierto en patrones nuevos sigue en 0.50–0.60 **aunque la lenta aprende la regla casi perfecta** (`Wps[0]` = 2.9,
   `Wns` ≈ 0.97 en los demás píxeles). Diagnóstico: **una puerta por magnitud no distingue "conocido" de "colado"**
   (una madre de veneno colada pesa −1, igual que una comida aprendida +1).
4. **Puerta definitiva, por familiaridad:** el patrón es familiar si **≥ `puerta` de las 3 celdas de su código tienen
   valor consolidado** (`|Wp − Wn| > 0.2`, **el mismo umbral que v11 usa para "consolidado"**; ninguna constante
   nueva). Se corre con `puerta = 2`. Un patrón entrenado tiene 3/3; uno nuevo, típicamente 0–1 colada.

**Diseño enmendado:** superficie `eta_s ∈ {0, 0.003, 0.006, 0.015, 0.03}` × **dos brazos** (`suma` = un error, y
`puerta = 2`), semillas 41–60, **todos los puntos se reportan**. El confirmatorio en 61–80 se hace con **un solo
punto** (el que mejor cumpla retención + E1 + E2 + E2L y luego acierto), y sólo él decide P4 y P5.

**Predicción del brazo `puerta`, escrita antes:** retención ≥ 18/20 en todo `eta_s` (la rápida manda en lo familiar);
acierto `px0` ≥ 0.80 con `eta_s ≥ 0.006` (lo nuevo va a la lenta, que es lineal); `xor01` ≤ 0.60; E1, E2, E2L ≥ 18/20.
**Riesgo declarado:** en E2 (inversión) y en el reencuentro del bloque M, el patrón sigue siendo familiar y la puerta
elige la rápida, que es lo correcto; el riesgo real es que patrones nuevos con **dos** celdas coladas pasen por
familiares y hereden un valor ajeno. Se mide con la fuga.

**Añadido antes de correr (humo con `puerta = 2`, semillas 41–42):** retiene (W_B −2.93/−2.95, W_A +1.00/+1.10) pero el
acierto queda en 0.60–0.70: con "2 de 3" todavía muchos patrones nuevos pasan por familiares (dos celdas coladas) y la
boca consulta la rápida. Se añade el punto **`puerta = 3`** (familiar sólo con las tres celdas consolidadas). La
superficie queda en **tres brazos × cinco tasas**, todos reportados; la predicción del brazo puerta se mantiene y se
espera que sea `puerta = 3` el que la cumpla.
