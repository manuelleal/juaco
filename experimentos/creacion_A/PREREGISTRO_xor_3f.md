# PREREGISTRO — Bloque 3f: XOR son TRES techos, no uno (borrador del CREADOR A para el coordinador)

**Estado:** borrador. No se corre nada de 3f hasta que el coordinador lo apruebe y le ponga semillas nuevas.
**Escrito el 18-sep-2026, ANTES de correr la serie.** Los números de "mini-prueba" de abajo son de humo (3 semillas,
un proceso) y **ya están medidos**; los de "predicción" **no**.

## 0. De dónde viene

Serie XOR del registro: 3 (dimensión ❌), 3b (puerta ❌), 3d (regla ❌), trío (tres mecanismos aislados ❌),
3e (identificabilidad / oráculo de rasgos ❌, 0.625). El diagnóstico que quedó escrito fue "el cuello es la dinámica".
El banco analítico del creador A (`experimentos/creacion_A/`, sección A del `PUENTE_creacion.md`) lo separa en **tres
techos independientes**, cada uno con su número, y el de la dinámica **no es el que manda**:

| # | techo | número medido | ¿lo mueve el resto? |
|---|---|---|---|
| (i) | **muestreo**: si una clase XOR no recibe mordidas, sus patrones de test quedan sin signo | mediana clavada en **0.750**; clase de tren vacía en **6/20** semillas | **no lo mueve nada**: ni tope, ni η, ni n = 5 000, ni AdaGrad, ni 1/√cuenta (0.750 en 12/12 combinaciones) |
| (ii) | **selección de rasgos**: con 8 patrones y 22 rasgos ninguna geometría de norma pasa de 0.56–0.62 | L2 0.562 · L1 0.625 · margen 0.500 · grado 0.531 · frecuencia 0.531 · **{6 px + P0·P1} = 1.000** | no lo mueve el tope (0.562 con `clip_s` 3, 10, 30, 100) ni el muestreo uniforme |
| (iii) | **tope `clip_s = 3`**: la solución de xor01 exige `\|w\| = 8` | con uniforme: satura en **0.625** con tope 3 y llega a **1.000** con tope ≥ 10 | **en el organismo NO manda** (medido: tope 3 → 30 no cambia nada) |

Y el hallazgo que ordena todo: **una vez abierto el rasgo correcto, no hay cuello de ajuste.** Con el conjunto
{6 px + P0·P1} la regla delta **online**, η = 0.015, sin trucos, llega al residuo **0.000** y a **1.000** de acierto.
*El ajuste está resuelto. Lo que falta es abrir el rasgo y que el mundo dé ejemplos de las cuatro clases.*

## 1. Hipótesis

**H3f.** `acc_lenta` en xor01 (nunca vistos, sonda a priori, `signo_acc` del registro) cruza **0.75 de mediana** si y
sólo si se quitan **a la vez** los tres techos. Cada pieza sola queda **≤ 0.65**.

## 2. Mundo, instrumentos, brazos

- Mundo de regla de siempre (`split_regla`, 20 patrones de peso 3, `ntr=(4,4)`), T = 200 000, `puerta = 3`.
- **Instrumento (ii)+(iii):** `experimentos/creacion_A/organismo_v13q4.py` (`3cc732dd2b2519cd`), por anclas desde
  `organismo_v13q3.py` (`aaebe073308a40c2`) con `construye_v13q4.py`. **Identidad con `seleccion=None` ≡ v13q3:
  16/16** (8 escenarios × 2 semillas, 38 claves, T = 30 000; incluye `oraculo01`, `delta_signo`, mundo 'AB',
  inversión, `eta_s = 0`, `random15`) — arnés `identidad_v13q4.py`.
- **Instrumento (i): NO EXISTE.** Ver §6.
- Brazos (todos con `lectura='cuadratica'`, `constante=True`, `regla_lenta='delta_signo'`, `lam_lenta=0`,
  `eta_s=0.05`):

| brazo | (i) muestreo | (ii) selección | (iii) tope | qué prueba |
|---|---|---|---|---|
| `BASE` | — | — | `clip_s=3` | el 3d/3e con el tope de fábrica |
| `T` | — | — | `clip_s=10` | la pieza (iii) sola |
| `S` | — | `seleccion='wta'` | `clip_s=3` | la pieza (ii) sola |
| `ST` | — | `seleccion='wta'` | `clip_s=10` | (ii)+(iii) — **lo que ya medí en humo** |
| `MST` | mecanismo del creador C | `seleccion='wta'` | `clip_s=10` | las tres |
| `ORAC` | — | rasgos dados (`lectura='oraculo01'`) | `clip_s=10` | referencia: el 3e con el tope subido |
| `RUIDO` | — | `seleccion='wta'` sobre `random15` | `clip_s=10` | **control**: si sube, la selección memoriza |

Reglas del mundo en cada brazo: **`xor01`, `px0` y `azar`**, las tres, siempre.

## 3. Predicciones numéricas (escritas antes de correr; 20 semillas nuevas, mediana + rango)

- **P1 (la que decide):** `MST` en xor01 **≥ 0.75** de mediana y **> `BASE` en ≥ 15/20** pareado.
- **P2:** cada pieza sola ≤ 0.65: `T` ≤ 0.65, `S` ≤ 0.65.
- **P3 (ya casi medida):** `ST` en **0.60–0.70** (humo: 0.625) — es decir, **no** alcanza sin (i).
- **P4 controles de regla:** `px0` **1.000** en todos los brazos; `azar` en **[0.35, 0.65]** en todos.
- **P5 control de memorización:** `RUIDO` ≤ 0.55 en xor01. Si `RUIDO` sube con la selección, el mecanismo memoriza y
  3f queda refutado aunque P1 pase.
- **P6 mecánica:** en `MST`, `|Ws(P0·P1)|` ≥ 4 en ≥ 12/20 (hoy no pasa de 3.1) y el conjuntivo abierto es `P0·P1`
  en ≥ 12/20 (hoy 1/3 y 2/3 en humo, 12–13/20 en el banco).
- **P7 (dinámica, ya no es incógnita):** con el rasgo correcto abierto y las cuatro clases mordidas, el residuo del
  ajuste online cae a ≈ 0 y el acierto a 1.000 (banco). Si en `MST` el rasgo se abre, las clases se muerden y aun así
  el acierto no sube, **mi modelo del ajuste está mal y hay que decirlo**.

## 4. Criterio de refutación

3f queda **refutado** si `MST` < 0.70 de mediana con `RUIDO` ≤ 0.55 y los controles de regla en su sitio. Si
`MST` ∈ [0.70, 0.75) se reporta como **progreso real**, sin recalibrar: se registra el número y se cierra la serie.
**No se barre `sel_theta` ni `sel_rho` después de ver los datos**; si hace falta barrerlos, se barren ANTES en
semillas distintas de las de la serie y se declara en el registro.

## 5. Cláusula del techo de muestreo 0.75 (importante: es RESULTADO, no fallo)

Si el mecanismo de (i) no cambia las proporciones de mordidas por clase, **0.75 es el techo y así se declara**:
*"con una clase XOR sin morder, el acierto balanceado en los nunca vistos no puede pasar de ~0.75; el límite es del
mundo y del canal de refuerzo (sólo se aprende al morder), no de la regla local"*. En ese caso:
- el objetivo de P1 baja a **≥ 0.72** (declarado aquí, antes de correr, como escenario alternativo preregistrado),
- y la línea XOR se cierra con vocabulario: *XOR es representable, legible, seleccionable y ajustable con reglas
  locales; lo que falta es que el mundo dé ejemplos de las cuatro clases*.
No se recalibra nada más: si `MST` < 0.72 con el mecanismo de (i) puesto, 3f cae.

## 6. Lo que 3f necesita del creador C (pieza (i)) — sin esto el bloque no se corre

La pieza (i) **no tiene instrumento**. Necesita un mecanismo que dé a la vía lenta ejemplos de las clases que hoy no
muerde, **sin cambiar el mundo** (trampa 3 de `EQUIPO.md`) y **sin inventar un canal de recompensa** (el Agente C del
puente XOR ya mostró que usar `R = 0` en un rechazo es contraproducente: borra lo aprendido). El candidato natural es
el frente del creador C: **aprender por PREDICCIÓN y no sólo al morder** — que la vía lenta se actualice con el error
de predecir lo que va a sentir, que sí ocurre en cada encuentro (incluidos los rechazos), no sólo en las ~330–660
mordidas. Dato duro para dimensionarlo: el Agente C midió `vis`/`mord` = comida `10` 481/428 (89 %) contra veneno
`00` 5 740/74 (1.3 %) — **hay 5 740 encuentros donde hoy no se aprende nada**. Si la vía lenta aprendiera en una
fracción de ellos, la pieza (i) se cae sola.

## 7. Coste

7 brazos × 3 reglas × 20 semillas = 420 corridas de T = 200 000. Con `organismo_v13q_rapido` (gemelo bit a bit) son
minutos; en Python puro, ~1.5 h·CPU con `Pool`. **El gemelo no tiene la perilla `seleccion`: hay que ampliarlo y
repetir su arnés, o correr en Python puro.** Decide el coordinador.

## 8. Lo ya medido (humo, 3 semillas, T = 200 000, un proceso — NO es la serie)

| brazo | xor01 s1/s2/s3 | mediana | px0 | azar |
|---|---|---|---|---|
| `BASE` (tope 3, sin selección) — de 3d/3e | — | 0.500–0.562 (registro) | 1.000 | 0.500 |
| `T` (tope 10, oráculo) | 0.625 / 0.500 / 1.000 | 0.625 | — | — |
| `T` (tope 30, oráculo) | 0.625 / 0.500 / 1.000 | 0.625 | — | — |
| `ST` `sel_estad='cond'` | 0.625 / 0.438 / 0.625 | **0.625** | **1.000** | **0.500** |
| `ST` `sel_estad='cov'` | 0.375 / 0.438 / 0.375 | 0.438 | — | — |
| sin selección, tope 10 | 0.500 / 0.312 / 0.562 | 0.500 | — | — |

Archivos del humo: `mini_prueba_A_seleccion.py`, `mini_prueba_A_tope.py`, `mini_seleccion.json`, `mini_tope.json`.
