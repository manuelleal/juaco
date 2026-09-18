# PREREGISTRO (borrador) — Mini-equipo 3, sala de enjambre: M3, memoria de un golpe por combinación

**Estado: BORRADOR de un mini-equipo, con mini-prueba de humo ya corrida (semillas 1-3, un proceso, sin Pool).
NO es la serie confirmatoria.** La serie (semillas 121–140, `Pool`) la decide y corre el coordinador. Escrito
18-sep-2026 por el mini-equipo 3 de la sala de enjambre (10-20 agentes, orquestador de equipo), a partir del
mecanismo entregado por el jefe de investigación. Misión del equipo (no opcional, `registro/EQUIPO.md` regla 13):
llegar a la AGI por este camino — un organismo mínimo con reglas locales, sin retropropagación, que sube la
escalera del brief con cada peldaño preregistrado, medido con controles y replicado; el método manda sobre el
cómo. **Recordatorio obligatorio (`CLAUDE.md` regla 8): nada de lo medido aquí declara AGI, conciencia ni
inteligencia general. Vocabulario permitido: aprende, revierte, extingue, generaliza, transfiere — sólo cuando el
criterio preregistrado lo respalde.**

## 1. De dónde viene

Serie XOR de creación A: 3/3b/3d/trío/3e (dinámica ❌, 0.625 con rasgos dados) → **control positivo**: el gradiente
exacto sobre el mismo flujo de encuentros llega a 1.000 (oráculo) — el cuello es la REGLA, no el mundo ni la
dimensión. Bloque A-4 (`eta_s`=0.15, `clip_s`=10, ya en el tronco v14.1): con rasgos dados la regla `delta_signo`
local llega a 1.000 pero necesita **150 exposiciones**; con rasgos propios (cuadrática) sigue en 0.50–0.63 porque
el organismo no construye el rasgo conjuntivo P0·P1 solo (WTA meta-aprendido lo abre en 11/20). **El cuello que
queda:** construir el rasgo conjuntivo con reglas locales y en pocas exposiciones.

La sala de enjambre corre esto en paralelo con mini-equipos independientes (grupos con mecanismos distintos);
este preregistro cubre **sólo el mecanismo M3** de este mini-equipo, en su propia carpeta
(`experimentos/enjambre/grupo3/`), sin tocar el tronco ni las carpetas de otros grupos.

## 2. Hipótesis

**H-M3.** El cuello de "pocas exposiciones" en XOR es el ESTIMADOR de la vía lenta, no la tasa: una regla que
escribe DE UN GOLPE el valor de cada combinación de 2 píxeles (en vez de acercarse a él con una tasa `eta_s`,
mordida a mordida) resuelve `xor01` en un puñado de exposiciones, sin memoria nueva relevante (135 números fijos:
15 celdas × 4 casillas + 15 bits de visitado + 15 medias de error) y sin tocar el tronco.

## 3. Mecanismo y memoria: M3 — memoria de un golpe por combinación

Cada una de las **15 celdas de dos canales** (todos los pares no ordenados `(i,j)` de los 6 píxeles binarios de
la retina, `i<j`) tiene **4 casillas de valor**, una por combinación `(P_i,P_j) ∈ {0,1}×{0,1}`. En cada mordida
`(P,R)`, **todas** las celdas actualizan su casilla correspondiente a la vez:

- dirección `k = 2·P_i + P_j ∈ {0,1,2,3}`;
- predicción `p_c = MM[c,k]` si `MN[c,k]>0`, si no **0.0** (abstención explícita: nunca "inventa" un valor);
- error propio `E_c ← (1-mem_rho)·E_c + mem_rho·(R-p_c)²` (la primera vez que la celda ve cualquier combinación,
  `E_c` se fija directo a `(R-p_c)²`, sin mezclar con el centinela inicial `1e9`);
- escritura: si `MN[c,k]==0` → `MM[c,k] = R` **DE UN GOLPE** (un solo ensayo, sin tasa); si no →
  `MM[c,k] += mem_alfa·(R-MM[c,k])` (brazo `'combi'`) o **no hace nada** (brazo `'combi1'`, binario literal: el
  primer valor queda para siempre); `MN[c,k] += 1`.
- **celda ganadora** = `argmin_c E_c`; **sólo ella** alimenta `lenta(P)` (lectura de la vía lenta que usa la boca).

Constantes: `mem_alfa=0.3`, `mem_rho=0.02`. Señal: **R de la mordida, y sólo eso** — no hay gradiente, no hay
tasa de aprendizaje, no hay error por unidad de la lectura completa: es una tabla de contenido-direccionable.
`memoria=None` desactiva todo (organismo_v13q5.py exacto). `lectura`/`phi(P)` **no** intervienen en M3 — `lenta(P)`
lee `P[i],P[j]` crudos, no `phi(P)` — declarado, no reclamado (ver §8).

**Fundamento:**
- Bittner, Milstein, Grienberger, Romani & Magee (2017), "Behavioral time scale synaptic plasticity underlies
  CA1 place fields", *Science* 357:1033-1036. BTSP: una sola coincidencia entre una traza larga y un evento de
  meseta escribe un campo de lugar de novo, en UN ensayo, sin repetición hebbiana.
- Milstein et al. (2024), "A simple model for BTSP provides content addressable memory with binary synapses and
  one-shot learning", *Nature Communications* (preprint bioRxiv 2023.04.04.535572). Memoria direccionable por
  contenido con sinapsis binarias, aprendizaje de una sola vez — el brazo `'combi1'`.
- Hernández-Cano, Matsumoto, Ping & Imani (2021), "OnlineHD: single-pass online learning using hyperdimensional
  system", DATE 2021 (código: github.com/BIASLab-UCI/onlinehd). Prototipos por clase aprendidos en UNA pasada.
- Hattori, Aso, Swartz, Rubin, Abbott & Axel (2017), "Representations of novelty and familiarity in a mushroom
  body compartment", *Cell* 169:956-969. La abstención como señal separada del valor.

**Traducción al organismo:** una celda que mira 2 píxeles binarios sólo tiene 4 entradas posibles, así que su
"traza de elegibilidad + meseta" se reduce a una casilla por combinación. El tercer factor es la mordida misma
(la puerta binaria "hay refuerzo ahora"), la misma forma que ya tiene la puerta por evidencia del código de v14.

## 4. Instrumento

- **Origen (sólo lectura):** `experimentos/creacion_A/organismo_v13q5.py`, sha256[:16] = `fae9c32b146fdbb4`
  (verificado antes de construir: coincide).
- **Construido por anclas:** `experimentos/enjambre/grupo3/construye_grupo3.py` → `organismo_g3.py`
  (sha256[:16] = `91eb167023cb37b7`). 5 anclas, todas con `assert src.count(A)==1` (conteo exacto verificado, no
  supuesto): (1) firma, añade `memoria=None,mem_alfa=0.3,mem_rho=0.02`; (2) estado, las 15 celdas (`_PAR`, `_MM`,
  `_MN`, `_ME`, `_MG`), antes de `Ws=np.zeros(_NF)`; (3) lectura, dentro de `def lenta(P):`, ANTES de la línea
  original (que queda intacta); (4) regla, rama nueva `if memoria is not None: ... elif seleccion is not None:`
  (la rama original de selección pasa a `elif`, sin tocarse); (5) return, añade `mem_ganadora`, `mem_tabla`,
  `mem_vistas`. Con `memoria=None` no se ejecuta ninguna línea nueva dentro del bucle salvo declarar arrays que
  nadie lee — identidad bit a bit esperada, y medida (ver abajo).
- **Identidad (`identidad_g3.py`, corrida ANTES de mirar cualquier número de la mini-prueba): 18/18.**
  9/9 obligatorios (`xor01`/`px0`/`azar` × semillas 1-3, T=30000, config del tronco v14.1) + 5/5 bonus (mundo
  `'AB'` tronco y por defecto, `lab=True`, `lineal`+`dos_canales`, `seleccion='wta'`) + firma (43 parámetros de
  `organismo_v13q5.run` son prefijo exacto de los 46 de `organismo_g3.run`) + validación (`memoria='no_existe'`
  lanza `ValueError`) + humo de que la perilla SÍ hace algo (`memoria='combi'`/`'combi1'` cambian
  `W_lenta_apriori` respecto de `memoria=None`, y escriben `mem_vistas>0`). Las únicas claves nuevas en TODOS los
  casos: exactamente `mem_ganadora`, `mem_tabla`, `mem_vistas` (ninguna otra clave cambió de nombre ni se perdió).
- **DOS BRAZOS HERMANOS:** `memoria='combi'` (promedio con `mem_alfa` tras la primera escritura) y
  `memoria='combi1'` (binario literal, Milstein 2024). Se corren los dos siempre.
- Sin `--rapido` (no hay gemelo compilado de esta línea; todo interpretado, igual que `organismo_v13q5`).

## 5. Predicciones numéricas — la del jefe y la mía corregida (con la mini-prueba de 3 semillas ya en mano)

**Del jefe (preregistrada ANTES de la mini-prueba, semillas 121–140, 20 semillas):**
- `acc_lenta` xor01 mediana **1.000**; ≥0.75 en **≥16/20** (puntuación del registro) y **≥11/20** (estricta);
  celda ganadora **(0,1)** en **≥18/20**; **n\* ≤ 20**.
- **Refutación:** si `n* > 60` o la mediana `< 0.875`, M3 cae.

**La mía, corregida con la mini-prueba (3 semillas, sección 8 — NO reemplaza la del jefe, la acompaña; ninguna
se recalibra después de la serie real, esto es ANTES):** con sólo 1/3 semillas teniendo las 4 clases
`(P0,P1)` en el entrenamiento (contra el 14/20 del control positivo por replay), espero que la fracción de
semillas 121–140 con las 4 clases sea del orden de 50-70%, así que:
- `acc_lenta` xor01 mediana en **[0.75, 1.00]** (puntuación del registro) — probablemente **por debajo** de 1.000
  por el efecto de abstención en las semillas sin las 4 clases; **estricta** bastante más baja, en **[0.50, 0.80]**
  — la mini-prueba dio 0.625, con sólo 1/3 semillas ≥0.75 en estricta.
- celda ganadora (0,1) en **≥17/20** (la mini-prueba dio 3/3).
- **n\* en [4, 16]** (la mini-prueba dio 7, cerca del 8 declarado por el jefe con el replay de 20 semillas).
- Mantengo el criterio de refutación del jefe (`n*>60` o mediana `<0.875`) para la serie real de 20 semillas —
  **no** para esta mini-prueba de 3, que es demasiado chica para decidir nada (una sola semilla mueve la mediana
  de 3 en 0.25).

## 6. Criterio de refutación (igual al del jefe, para la serie de 20 semillas)

M3 queda refutado si, en semillas 121–140: `n* > 60`, o la mediana de `acc_lenta` (puntuación del registro)
`< 0.875`. Con `n* > 60` **y** mediana `≥ 0.875`, se reporta como lectura mixta y se decide con el auditor.
Controles obligatorios que deben pasar a la vez (§7): `px0 = 1.000` en 20/20 y `azar` con mediana en [0.35,0.65].

## 7. Controles que pueden fallar

1. **Abstención infla el 20/20 (declarado por el jefe, MEDIDO aquí):** en la mini-prueba, sólo **1/3** semillas
   tuvo las 4 clases `(P0,P1)` en el entrenamiento; con puntuación del registro (empate=0.5) las 3/3 semillas
   pasan ≥0.75 igual, pero con puntuación **estricta** (empate=0) sólo **1/3** pasa (mediana 0.8125→0.625). Se
   reportan SIEMPRE las dos puntuaciones y el subconjunto de semillas con las 4 clases, y no se declara
   "resuelve XOR" sólo con la puntuación del registro.
2. **Coste conductual de la abstención (declarado por el jefe; mini-chequeo aparte, `memoria=None` vs `'combi'`,
   mismas 9 combinaciones semilla×regla, T=100000 completo):** muertes 128,131,132,158,139,130,153,147,137
   (`None`, mediana 137) contra 124,102,117,136,151,142,143,140,143 (`'combi'`, mediana 140) — **sin señal clara
   de coste** en esta comparación pequeña y no diseñada para esto (n=9, sin semillas pareadas por regla-condición
   controlada de verdad); mordidas totales tampoco muestran un patrón consistente (suben en `azar`, bajan en
   `xor01`, mixto en `px0`). **No es evidencia fuerte en ningún sentido — queda para el control formal en la
   serie real**, con las métricas completas (veneno comido, energía, muertes) por brazo.
3. **Azar, sobreajuste con 15 hipótesis y escritura de un golpe (declarado por el jefe, MEDIDO — y CONFIRMADO):**
   mediana 0.5 [0.2, 0.5] (dentro de [0.35,0.65]), **pero la semilla 2 dio 0.2 en AMBOS brazos**, por debajo del
   umbral individual — exactamente el riesgo que el jefe declaró ANTES de correr ("una semilla dio 0.2, por
   debajo del azar"). El criterio de la serie es sobre la MEDIANA de 20, no cada semilla; esto se reporta para
   que quede escrito, no para relajar el criterio.
4. **px0 = 1.000:** en 6/6 corridas de la mini-prueba (3 semillas × 2 brazos). OK.
5. **Identidad con `memoria=None`:** 18/18 (§4), incluida la validación del knob y la firma. OK.
6. **Riesgo de flujo (declarado por el jefe, MEDIDO — CONFIRMADO en `azar`, no en `xor01`/`px0`):** en `xor01` y
   `px0` (reglas deterministas por combinación), `'combi'` y `'combi1'` dieron el MISMO número de eventos
   pre-sonda, la MISMA celda ganadora y la MISMA `acc_lenta` en las 3 semillas — no hay margen para que diverjan,
   porque cualquier casilla que se reescriba recibe siempre el mismo R. En `azar` SÍ divergen: p.ej. semilla 1,
   `'combi'` tuvo 264 eventos pre-sonda y ganó la celda (0,2); `'combi1'` tuvo 160 eventos y ganó la celda (2,4)
   — la vía lenta, al aprender distinto, cambia CUÁNTO muerde la boca antes de la sonda, y eso realimenta qué
   celda gana. Confirma el mecanismo del riesgo, no lo refuta ni lo agrava para `xor01` (la línea que importa).
7. **M1 como control interno (declarado por el jefe):** NO comparado aquí — está fuera del alcance de un solo
   mini-equipo trabajando sólo en su carpeta; lo hace el coordinador al integrar los grupos de la sala.
8. **`lectura` es inerte para M3, declarado (no reclamado):** `lenta(P)` con `memoria` activa lee `P[i],P[j]`
   crudos, nunca `phi(P)`; `lectura='cuadratica'` no cambia ni un número de M3 (se usó por instrucción, nunca
   `'oraculo01'`). Confirmado por construcción (ancla 3) y por la identidad (casos `lineal_dos_canales` y
   `AB_defecto` en §4, que ejercitan `lectura` distinta sin tocar M3 porque `memoria=None` ahí).

## 8. Mini-prueba ya corrida (`mini_g3.py`, un proceso, sin Pool, semillas 1-3, T=100000) — NO es la serie

`python experimentos/enjambre/grupo3/mini_g3.py` → `mini_g3_20260918_064248.{log,json}`, 158.1 s total (18
corridas de T=100000 + réplicas de exposiciones). **Verificación del replay: 18/18 casos coinciden EXACTO
(diferencia 0) contra `W_lenta_apriori` del organismo** — el método de exposiciones es de fiar.

| regla | brazo | acc_lenta (mediana [rango]) | estricta | ≥0.75 (registro/estricta) | ganadora (0,1) | 4 clases en tren | n\*(≥0.75) |
|---|---|---|---|---|---|---|---|
| xor01 | combi | 0.8125 [0.75, 1.00] | 0.625 [0.50, 1.00] | 3/3 · 1/3 | 3/3 | 1/3 | **7** |
| xor01 | combi1 | 0.8125 [0.75, 1.00] | 0.625 [0.50, 1.00] | 3/3 · 1/3 | 3/3 | 1/3 | **7** |
| px0 | combi | 1.000 [1.00, 1.00] | 1.000 | 3/3 · 3/3 | 1/3 (gana pixel 0 igual) | 3/3 | 2 |
| px0 | combi1 | 1.000 [1.00, 1.00] | 1.000 | 3/3 · 3/3 | 1/3 | 3/3 | 2 |
| azar | combi | 0.5 [0.20, 0.50] | 0.5 [0.20, 0.50] | 0/3 · 0/3 | 0/3 | 3/3 | >600 |
| azar | combi1 | 0.5 [0.20, 0.50] | 0.5 [0.20, 0.50] | 0/3 · 0/3 | 0/3 | 3/3 | >600 |

Curva de exposiciones xor01 (mediana de 3 semillas, puntuación del registro): n=1→0.56, 2→0.62, 3→0.62, 4→0.72,
5→0.72, 6→0.72, **7→0.81**, 8→0.81 ... se mantiene en 0.81 hasta n=30 (el techo de esta mini-muestra: 2/3
semillas nunca llegan a las 4 clases, así que el registro no puede subir de 0.81 con más exposiciones — lo tapona
la abstención, no la falta de datos). px0 llega a 1.000 en n=16.

Con 3 semillas **no se ajusta ni se decide nada** (una semilla cambia la mediana en 0.25). Lo que sí queda
declarado: `n*` de un solo dígito (7, contra 150-200 de A-4 con rasgos regalados y contra 10 del gradiente
exacto/control positivo) es consistente con la predicción central del mecanismo — el estimador, no la tasa, era
el cuello —, y el patrón de fallos (abstención, azar al filo) es exactamente el que el mecanismo predijo, no uno
nuevo.

## 9. Coste de la serie real

20 semillas × 3 reglas × 2 brazos = 120 corridas de T=100000 (+ identidad y réplica del replay). Medido en la
mini-prueba: **~8.7 s por corrida en un proceso** (con `lab=True` y `T=100000`). Con `Pool` (14, como A-4):
≈ 120 × 8.7 / 14 ≈ **75 s** más arranque — barato; lo caro sería si el coordinador pide además el control de
coste conductual completo (§7.2) contra `memoria=None`, que dobla las corridas.

## 10. Vocabulario, si la serie pasa

*"La vía lenta, con una tabla de contenido-direccionable de 15 celdas de dos canales que escribe de un golpe,
generaliza xor01 en un puñado de exposiciones (n\* de un dígito), sin memoria nueva relevante y sin tocar el
tronco."* Nada de "aprende XOR" mientras la puntuación estricta se quede por debajo de 0.875 en la mediana de
20 semillas, ni "resuelve" mientras el control de abstención (§7.1) no se reporte al lado. Nada de AGI, conciencia
ni inteligencia general por este ni ningún resultado (`CLAUDE.md` regla 8).
