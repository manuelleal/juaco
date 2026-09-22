# PREREGISTRO — FANIN: entradas por celda de la expansión Kenyon (6 / 3 / 2) — SELLADO 22-sep-2026 (§6d decidido)

Creador (Opus), 22-sep-2026, rama `rama-fanin` (worktree `JUACO/fanin`). Versión 2, con las seis correcciones del coordinador.
**La serie NO se ha corrido.** Los números de §11 son humo y mini-prueba en semillas quemadas (no son dato). Queda una decisión
abierta para el coordinador antes de sellar (§6d). Misión: llegar a la AGI por este camino; el método manda.

## 0. Texto del director (textual)

> **Hipótesis/predicción:** con 2 o 3 entradas por celda mejora el acierto en patrones nunca vistos, en el patrón negativo y en el XOR.
>
> "Predicción de costo: baja la generalización medida en la Etapa 3, porque menos entradas significan códigos menos solapados.
> Refutación: si no hay mejora en patrones nunca vistos, la hipótesis cae y el cuello del punto 4 sigue siendo de crecimiento, no de cableado.
> Por qué va primera: cuesta una tarde y, si sale, te ahorra el mecanismo de reclutar y fusionar entero."

**Lectura de la refutación (coordinador, así se escribe):** si no hay mejora, cae la hipótesis del CABLEADO (entradas por celda);
eso no demuestra por sí solo que el cuello sea de crecimiento, sólo que queda como la hipótesis viva. **Y sólo cae en los brazos
y pruebas que pasen la puerta de validez (§6b) y la de pool (§6c); en los demás el resultado es NO CONCLUYENTE, no refutación.**

## 1. Tronco y dónde está el parámetro

- Tronco vigente: **v14.2** (`organismo/organismo_v142.py` `17528d767fcebaf6`; manda `registro/ESTADO.md`; CLAUDE.md dice v14.1).
- La expansión es **densa**: `KW[:NK]=rng.uniform(0,1,(NK,6))`: cada una de las NK = 30 celdas lee **los 6 píxeles**; el código
  son las K = 3 celdas de mayor `KW@P` (`np.argsort(v)[-K:]`). **No existía perilla de entradas por celda.**
- **Perilla `fanin`** (defecto 6): con `fanin < 6` cada celda sorteada multiplica sus pesos por una máscara de `fanin` píxeles
  distintos, sorteada con **RNG propio** `default_rng(60000 + seed)`; el rng del organismo consume exactamente lo mismo que el
  tronco. Con 6 no hay máscara ni multiplicación.
- Decisiones declaradas: (1) la máscara vale para las 30 celdas sorteadas y sus re-sorteos en `cond()` (mundo AB); (2) las
  **hijas** nacen con la regla del tronco sin tocar (soporte `_rel` ⊆ píxeles encendidos del patrón que divide; se mide el fanin
  efectivo); (3) `solap_AB` (E2L) igual que en el tronco. NK = 30, NKMAX = 90. Memoria nueva: cero. Constantes nuevas: cero.
- **Desempate del "ganan K" (NO se cambia):** `np.argsort` por defecto (`quicksort` = introsort, **no estable**); entre valores
  exactamente iguales decide el orden interno de numpy (determinista para el mismo arreglo). No hay desempate explícito.

## 2. Instrumentos (por anclas, `construye_fanin.py`) e identidad

| archivo | origen (sha, congelado) | sha |
|---|---|---|
| `organismo_v142_fanin.py` | `organismo/organismo_v142.py` `17528d767fcebaf6` | `a1d97a02bdf9dec9` |
| `organismo_v142g_fanin.py` (+ mundo `rejilla`, conteo por vía) | `organismo/organismo_v142g.py` `9e5f566cd6a7a4d2` | `71e9b247ec1e91fc` |
| `bateria_v142_fanin.py` (examen v3') | `organismo/bateria_v142.py` `6375d90e531b06e6` | `5e3e5b3878881ddf` |
| `bateria_generaliza_v142_fanin.py` (Etapa 3) | `organismo/bateria_generaliza_v142.py` `e5929942647756a5` | `df13a4e65335ff10` |

**Identidad bit a bit con fanin = 6: 23/23** con estos sha (`identidad_fanin_salida.txt`): 7 escenarios del examen × semillas 1–2
(T = 100 000) contra `organismo_v142`; 3 reglas × 2 semillas (T = 200 000) contra `organismo_v142g` con los kwargs del tronco
leídos de la batería congelada (regla 14); `diag=True` inerte (3 casos, incluido el conteo nuevo por vía). El runner se niega a
correr si el sha del instrumento no es el del arnés en verde. Regla 14: entrada nueva de INSTRUMENTOS = copia literal de la del
tronco (verificada por el constructor); los dos humos de baterías escriben su JSON (el primero no: ERR-42 repetido, corregido).

## 3. Baterías: qué existía y qué se construye

| prueba | ¿existía? | aquí |
|---|---|---|
| XOR | sí: `xor01` del mundo de regla (peso 3; 8/12; tronco 0.438). La XOR "cerrada con prior de pares" es `creacion_A/xor_7` (M3, **no está en el tronco**) | `xor` en `rejilla` (principal) + `xor01` de la Etapa 3 (secundaria) |
| patrón negativo | **no existe** (sólo literatura) | `np` en `rejilla` |
| conjunción | **no existe** | `conj` en `rejilla`: **control de NO CAMBIA, no control positivo** (§3b) |
| paridad de tres | **no existe** | `par3` en `rejilla` |
| Etapa 3 | sí: `bateria_generaliza_v142` (px0 / azar; G1, G2, K) | en la serie, tres brazos, mismas semillas, **solapamiento al lado** |

**Mundo `rejilla`:** los 63 patrones no vacíos de 6 px. Píxeles relevantes `a, b, c` sorteados por semilla
(`default_rng(70000+seed)`). `conj` = a∧b · `np` = A+, B+, AB− (sin la fila 00: 48 patrones) · `xor` = a⊕b · `par3` = a⊕b⊕c ·
`px0` = a · `azar` = valencia al azar, mitad y mitad (`default_rng(80000+seed)`). Por qué no el mundo de peso 3: allí `np` sin
la fila 00 es lineal y `par3` tiene filas de una sola variante.

**3b. Controles positivos limpios (los tres brazos deben resolverlos):** `px0` de la **Etapa 3** (G1 de la batería del tronco:
lineal, el tronco da 1.000) y `px0` de la rejilla (lineal sin sesgo). **`conj` no es control positivo:** sin sesgo no es
separable (patrón "sólo a" < 0, "sólo b" < 0 y "a y b" > 0 es imposible con `(Wps−Wns)@P`); mini-prueba F6 0.458.

## 4. "La mitad de los patrones"

Por **filas** de la tabla de verdad el problema está **mal puesto** (una fila nunca vista no se puede inferir; por semejanza, XOR
y paridad darían **por debajo del azar**). **Aquí: por VARIANTES dentro de cada fila, todas las filas vistas:** en cada fila
`floor(n/2)` variantes al tren y el resto al test (`default_rng(90000+seed)`). Tren/test: conj, xor, azar, px0, par3 31/32;
np 24/24. Comida en test: 16 (conj 8 de 32 → acierto balanceado). Predicción escrita para la versión por filas (no implementada):
XOR y paridad < 0.50 en los tres brazos.

## 5. Brazos, semillas, T

Brazos **F6** (tronco), **F3**, **F2**. **Serie: semillas 6021–6040**, pareadas en los tres brazos. **6001–6020 quemadas**
(humo y exploración); **6901 quemada** (mini-pruebas). **Réplica (regla 12): 6041–6060.** Sin solape con repo ≤ 2360, carreras
3001–3299, 4001–4199, 5001–5020. T = 200 000, sonda a priori en T/2. kwargs del tronco (regla 14): `eta_s=0.15, clip_s=10.0,
puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1`, `desambiguar=1`. Por brazo,
además: examen v3' (`bateria_v142_fanin.py 20 --desde 6021`) y la Etapa 3 copiada.

## 6. Métricas y puertas (numéricas, antes de ver datos)

- **Principal:** `acc` = acierto de signo **balanceado** (valor 0 = 0.5) sobre las variantes de test, con el valor total que usa
  la boca, en la sonda a priori; J = 2·acc − 1 (regla 15).
- **Secundarias:** `acc_rapida` (vía rápida leída directamente), `acc_lenta`, `ba` (conducta al primer encuentro), acierto por
  fila, `alias_test`. **Diagnósticos:** cobertura, empates, solapamiento (todos, d = 1, d = 2; inicio/sonda/fin), códigos
  distintos, celdas usadas, impulso > 0, fanin efectivo.
- **6a. MEJORA** (F vs F6, pareado, por prueba): mediana ≥ **+0.05** **y** ≥ **15/20** suben (empates en contra) **y** signo
  exacto de una cola con **Holm** sobre 6 comparaciones (np, xor, par3 × F3, F2), p_Holm < 0.05. Nulo 0; margen 0.05; P(≥ 15/20 |
  nulo) = 0.021. **NO CAMBIA** (conj): |mediana| < 0.05 y signo de dos colas p ≥ 0.05. **Media de las 4:** misma puerta,
  Bonferroni ×2. **COSTO** (Etapa 3 px0): mediana ≤ −0.05, ≥ 15/20 bajan, p < 0.05 (Bonferroni ×2), más G1/G2/K por brazo;
  solapamiento en la sonda al lado.
- **6b. PUERTA DE VALIDEZ (coordinador).** Se mide por brazo y por prueba la fracción de ensayos que decide la **vía rápida**
  (la expansión): (i) en la **sonda** a priori, nunca vistos (`rapida_sonda_test`: los ensayos que puntúa la métrica principal)
  y vistos (`rapida_sonda_tren`); (ii) en **cada encuentro** desde T/2, nunca vistos al entrar (`rapida_enc_test`) y vistos
  (`rapida_enc_tren2`). **Puerta sobre (i): si en un brazo la mediana de `rapida_sonda_test` es < 0.30, ese brazo en esa prueba
  es NO CONCLUYENTE para la hipótesis del cableado** (ni la confirma ni la refuta). Una comparación F vs F6 es concluyente sólo si
  el brazo F pasa la validez y ni F ni F6 fallan la puerta de pool. F6 se reporta (su fracción es parte del tronco).
- **6c. PUERTA DE POOL.** Por brazo y prueba: celdas activas al final y paso en que el pool llega a 90 (`t_lleno`, de la
  identidad celdas = 30 + divisiones). **Si se llena antes de T/2 (fin del entrenamiento) en ≥ 10/20 semillas, se declara "mide
  capacidad"** y esa prueba es NO CONCLUYENTE para el cableado en ese brazo.
- **6d. DECISIÓN ABIERTA PARA EL COORDINADOR (antes de sellar).** Si la puerta 6b deja NO CONCLUYENTE casi todo (predicción
  C1-bis), la única lectura del cableado que no pasa por la puerta de familiaridad es `acc_rapida`. **Propongo** preregistrar ya
  la misma puerta de MEJORA (6a, con su Holm aparte) sobre `acc_rapida` como **análisis secundario del cableado de la
  representación**, sin sustituir el principal. No está aplicado en la letra de los veredictos: el runner lo calcula y lo imprime,
  pero no lo declara.
  **DECIDIDO por el coordinador (22-sep, antes de sellar): SÍ.** La puerta de MEJORA 6a se aplica también sobre `acc_rapida` como
  **análisis SECUNDARIO** del cableado de la representación, con su propia corrección de Holm sobre sus comparaciones. Tiene
  veredicto propio, pero **no sustituye al principal**: la hipótesis del director se juzga con el principal y el secundario solo
  se reporta como "lectura directa del cableado". Si el secundario pasa y el principal queda NO CONCLUYENTE, se declara así, sin
  convertirlo en confirmación. El runner ya lo calcula; la letra del veredicto secundario queda fijada aquí.
- **PLACEBO (regla 15):** la puerta 6a sobre F6(s) contra F6(s+1 cíclico): debe pasar **0 de 4**, o se abre ERR antes de leer.
- **Controles que pueden fallar** (cada brazo): rejilla `px0` ≥ 0.65, rejilla `azar` ∈ [0.35, 0.65] y **Etapa 3 G1 PASA**; si
  caen, el bloque no se lee.
- **Versión reducida del mundo (tope de variantes por fila, `regla@n`, todas las filas conservadas): NO se propone como
  preferida.** En la mini-prueba el pool del mundo completo se llena **después** de T/2 (xor: 112 034 y 110 648), y el tope no
  evita llenarlo (par3@4 F2 se llena en 76 004, antes de T/2; xor@8 F2 en 108 057; F6 llega a 79 y 89 celdas). Además reduce el
  test a la mitad. La perilla queda en el instrumento sin usar.

## 7. Predicciones, lado a lado

| | **Director (textual, §0)** | **Coordinador (refinadas)** | **Creador (mías; ver §11)** |
|---|---|---|---|
| nunca vistos (media de las 4) | mejora con F2 o F3 | — | **no pasa la puerta 6a** en ningún brazo |
| patrón negativo | mejora | (a) mejora con F2 y F3 | único candidato (F2); apuesto a que **no** pasa (mediana F2−F6 en [−0.05, +0.15]) |
| XOR | mejora | (a) mejora con F2 y F3 | **no** mejora (F6 en [0.45, 0.70]) |
| paridad-3 | — | (b) mejora **sólo** con F3 | **no** mejora; **por debajo del azar** en los tres brazos (F6 en [0.30, 0.50]) |
| conjunción | — | (c) no cambia (control) | no cambia; F6 en [0.40, 0.55] (**no es control positivo**) |
| partición por filas | — | (d) por debajo del azar | igual (no aplica: la partición es por variantes) |
| costo en la Etapa 3 | **baja** (códigos menos solapados) | — | **no baja** (px0 F−F6 en [−0.03, +0.10]; G1/G2/K pasan en los tres) |
| solapamiento (mecanismo) | baja | — | **baja** (Etapa 3, mediana ≤ −0.10 en ≥ 18/20): el mecanismo ocurre pero no cuesta |
| puerta de validez 6b | — | — | **C1-bis:** `rapida_sonda_test` muy variable: F6 [0.10, 0.45], F3 [0.00, 0.60], F2 [0.05, 0.70]; predigo **≥ 3 de las 6** celdas F3/F2 × (np, xor, par3) NO CONCLUYENTES |
| puerta de pool 6c | — | — | el pool se llena **después** de T/2 en < 10/20 en np, xor, conj; en par3 F2 puede caer (sin predicción firme) |
| examen v3' | — | — | F6 8/8; F3/F2 pasan identidad, 2, 3, 4a, 4b, 4d; 1 y 4c sin predicción firme (5/8–8/8) |

**Predicción mía refutada ya por la mini-prueba (se declara):** en la v1 predije que con F3/F2 "la puerta manda casi todo lo nunca
visto a la vía lenta" (fracción ≤ 0.20). Eso vale a T = 20 000 (humo), pero a T = 200 000 la semilla 6901 da F2 xor 0.56 contra
F6 0.12: con el tiempo largo, **F2 puede mandar MÁS a la expansión que F6**. La C1 original queda retirada; la reemplaza C1-bis.

## 8. Qué lo refuta

El cableado cae **sólo en las comparaciones concluyentes (6b, 6c)** si ninguna pasa MEJORA y la media de las 4 tampoco, con el
placebo 0/4 y los controles en su sitio. Si todas son NO CONCLUYENTES, la serie no decide el cableado y se dice así. El costo del
director cae si la Etapa 3 no baja por la puerta de COSTO. Mis predicciones se declaran una a una.

## 9. Las cuatro trampas

(1) **Canal simétrico:** máscara al azar por celda, igual para comida y veneno; la vía lenta no ve el fanin. (2) **Acierto sin
balancear:** todo acierto es balanceado, con J. (3) **Mundo que se come la comida:** `conj` da 4× menos comida (mini-prueba: 556
muertes); igual en los tres brazos; la medida principal es la sonda de valor. (4) **Sitios fijos:** píxeles relevantes
sorteados por semilla; aparición al azar.

## 10. Coste

Humo: 64.1 µs/paso. Serie: 540 corridas de 200 000 (1.9 h CPU) + examen v3' ×3 (1.9 h) + Etapa 3 copiada ×3 (0.4 h) ≈ **4.2 h de
CPU ≈ 42 min con Pool(6)**. `python experimentos/nivel07_fanin_expansion/corre_fanin.py --pool 6` (lo corre el coordinador;
semillas 6021–6040 por defecto).

## 11. Medido ya — NO es la serie (semillas quemadas)

**Humo** (`datos/humo/fanin_humo_20260922_132030.json` `aa8b4ff713e34c68`, con el runner final; los humos anteriores, superados,
en `datos/humo_no_registrado/`; un proceso; 3 brazos × 6001–6002; T = 20 000).
`rapida_sonda_test` (mediana): np 0.438 / 0.062 / 0.083 (F6/F3/F2); xor 0.266 / 0.000 / 0.016; par3 0.359 / 0.000 / 0.031;
conj 0.172 / 0.000 / 0.000; Etapa 3 px0 0.250 / 0.000 / 0.100. Pool: 34–62 celdas, **no se llena** en ninguna tarea (T corto).
Cobertura 6/6 en todos; lecturas mínimas por píxel 30 / 12 / 7. Empates 0 en la rejilla; en la Etapa 3 F3 0.008 y F2 0.029 de
las llamadas (máx 0.097), ninguno en valor 0 (causa no diagnosticada). Solapamiento en la sonda (Etapa 3) 0.336 / 0.149 / 0.133.
Controles OK en los tres brazos (incluido Etapa 3 G1); placebo 0/4.
**Mini-pruebas** (semilla 6901, T = 200 000): `mini_prueba_6901_salida.txt` (conj F6 0.458; np F6 0.531 / F2 0.750; xor F6 0.688 /
F2 0.531; par3 F3 0.375) y `mini_prueba_pool_6901_salida.txt` (rápida en la sonda, nunca vistos: xor F6 0.12, F2 0.56; xor@8
F6 0.25, F2 0.31; par3@4 F6 0.19, F2 0.69. Pool lleno: xor F6 112 034, F2 110 648; xor@8 F6 no (79), F2 108 057; par3@4 F6 no
(89), F2 76 004).

## 12. Lo que no cubre

No toca el crecimiento (reclutar/fusionar) ni la puerta de familiaridad; no prueba fanin 1, 4 ni 5; no cambia el desempate. Si
6b deja todo NO CONCLUYENTE, el bloque siguiente natural es medir la expansión con la puerta abierta (otro cambio, otro
preregistro).
