# Bloque 3e: ¿el límite de XOR es la REGLA o la SELECCIÓN DE RASGOS? — lectura oráculo (escrito ANTES de correr; semillas 61–80)

**17 sep 2026, noche.** 3d salió **refutado** (`xor_3d_s41-60_20260917_225535`, JSON `3e2489b1b02d4f19`): la regla fusionada
del trío (`phi' = phi+[1]`, vector con signo `Ws`, decaimiento `lam_lenta = 0.002`) da `acc_lenta` mediana **0.500**
[0.25, 0.81] en `xor01` — **exactamente lo mismo que los dos canales** (CUAD_2C 0.500), y sólo gana pareado en **5/20**.
Z2 y Z3 pasaron (controles y regresión intactos), Z4 cayó 1/20: el producto sí se aprende (`Ws(P0·P1)` = −0.83 en la
sonda) y **los marginales siguen en cero** (`Ws(P0)` = −0.00, `Ws(P1)` = −0.29). La curva preregistrada **no** lo
explica: con las 4 clases mordidas (n = 17) la mediana sigue siendo 0.500. Tres reglas distintas dan el mismo número:
**el sospechoso ya no es la regla**.

Lectura del coordinador con `registro/investigacion/xor_mecanismos_locales_20260917.md` (mecanismo 3, que es **dato
citado, no instrucción** — EQUIPO regla 8): con **8 patrones de entrenamiento** en `xor01` (`ntr = (4,4)`; 10 en
`px0`/`azar`) y **21–22 rasgos**, el problema está **indeterminado**: infinitas soluciones ajustan el tren y casi
ninguna generaliza. El mismo informe cita a Cover (1965) y a Bengio/Delalleau/Le Roux (2006) y Daniely & Malach (2020)
para lo que ya está medido aquí (`random15` = 0.500, plano): en paridad no falta tamaño, falta **la interacción
correcta**; el mínimo real es d = 3 (`P0, P1, P0·P1`) o 4 con sesgo, y predice que una `phi` mínima superaría 0.60.

## Hipótesis (una sola, decisiva)
Si a la MISMA regla local (delta con signo + constante + decaimiento 0.002, sin tocar nada más) se le dan **sólo los
tres rasgos correctos**, separa XOR en nunca vistos. Entonces el límite de v13 no es la regla de la vía lenta sino
**qué rasgos tiene** — un problema de sesgo inductivo / selección de rasgos.

## Instrumento (enmienda por anclas al mismo constructor, no una copia nueva)
`construye_xor_3d.py` (ahora `61c6c537a224dbea`) añade dos lecturas a `organismo_v13q3.py` (ahora **`aaebe073308a40c2`**;
el de 3d era `b71bbe41a7326aaf`):
- **`lectura='oraculo01'`**: `phi(P) = [P0, P1, P0·P1]` — 3 entradas, **4 con `constante=True`**. Es la base exacta de
  `xor01`. **Es una trampa deliberada**: se le regalan los rasgos para ver si la regla puede con ellos.
- **`lectura='oraculo01_ruido'`**: `phi(P) = [P0, P1, P2·P3]` — **control**: mismo tamaño, mismos marginales, el
  **producto equivocado**.
- `lectura` mal escrita levanta `ValueError` (no puede caer en silencio a `random15`).

**Dos identidades, las dos verificadas antes de escribir esto:**
1. Con los knobs en su valor original (`dos_canales`, `constante=False`), `organismo_v13q3` ≡ `organismo_v13q` en todas
   las claves del original (4/4 en el humo; 12/12 en la ETAPA 1a del runner).
2. **Inercia:** la enmienda 3e no cambia **nada** de 3d — **16/16 corridas idénticas** (CUAD_DELTA, CUAD_2C, LIN_DELTA,
   RANDOM15_DELTA × `xor01`/`px0` × 2 semillas, T = 30 000) contra una copia bit a bit del instrumento con el que se
   corrió 3d (`b71bbe41a7326aaf`). El runner repite esta comprobación (ETAPA 1b) contra los **números publicados** de
   3d (`datos/xor_3d_s41-60_*.json`, semillas 41–43) y se para si difieren: los resultados de 3d siguen siendo
   reproducibles con el instrumento enmendado.

## Brazos (mundo de regla, `puerta = 3`, `eta_s = 0.015`, `T = 100 000`, `lam_lenta = 0.002`, semillas NUEVAS 61–80)
**La BASE es idéntica a la de 3d: entre CUAD_DELTA y ORACULO_DELTA lo ÚNICO que cambia son los rasgos de `phi`.**

| brazo | `lectura` (rasgos) | `regla_lenta` | `constante` | para qué |
|---|---|---|---|---|
| **ORACULO_DELTA** | `oraculo01` → `[P0, P1, P0·P1, 1]` | delta_signo | True | la regla de 3d con los rasgos exactos |
| **RUIDO_DELTA** | `oraculo01_ruido` → `[P0, P1, P2·P3, 1]` | delta_signo | True | **control**: mismo tamaño, producto equivocado |
| **ORACULO_2C** | `oraculo01` → `[P0, P1, P0·P1]` | dos_canales | False | ¿la regla **original** de v13 también puede con los rasgos exactos? |
| **ORACULO_2C_CTE** | `oraculo01` → `[P0, P1, P0·P1, 1]` | dos_canales | True | separa "regla" de "constante" bajo el oráculo (descriptivo, añadido por el diseñador) |
| **CUAD_DELTA** | `cuadratica` (22) | delta_signo | True | referencia: el brazo refutado en 3d, re-corrido en semillas nuevas |

Reglas: `xor01` y `px0`. **5 × 2 × 20 = 200 corridas** de T = 100 000 (+ 12 de identidad + 3 de inercia). ~2 min con `Pool(14)`.

## Medidas
Las de 3d, sobre los nunca vistos en la sonda de `fase2_en`: `acc` (valor total), **`acc_lenta`** (vía lenta sola), `ba`,
`cobertura`, y desde `Ws_apriori` (pesos **en la sonda**, no al final de `T`): `Ws(P0)`, `Ws(P1)`, **`Ws(prod)`** —
índice 2 con oráculo, 6 con cuadrática, y el campo `prod_es` dice cuál es (`P0*P1` o `P2*P3`), que **no es el mismo
rasgo** en RUIDO_DELTA — `Ws(cte)`, **`max|Ws|`** y `clases_sin_morder`.

## Criterio (**único**, escrito antes de correr)
**O1:** ORACULO_DELTA `xor01` **`acc_lenta` mediana ≥ 0.80** **y** > RUIDO_DELTA **pareado ≥ 15/20**.
El contraste de O1 **mantiene la regla fija y varía sólo los rasgos** (mismo `phi` de tamaño 4, mismo aprendizaje, misma
semilla): es exactamente la pregunta "¿regla o rasgos?". Todo lo demás de este preregistro es lectura, no criterio.

**R1 (lectura obligatoria, NO decide el veredicto):** ORACULO_DELTA `px0` `acc_lenta` ≥ 0.65. **Ojo, y por eso se
escribe:** el oráculo **no** es ciego a `px0` — `P0` **es** el píxel 0, así que la base `[P0, P1, P0·P1, 1]` contiene la
regla `px0` entera y `px0` debe seguir **alto** (0.90–1.00), igual que en 3d. **`px0` no discrimina entre brazos en 3e**
(RUIDO_DELTA también lleva `P0`, así que también estará alto): es una comprobación de que el instrumento no se rompió,
no un control que pueda fallar en la dirección informativa. Leerlo como "el control pasa" sería un error de lectura.

## Predicción numérica
| medida | predicción | de dónde |
|---|---|---|
| ORACULO_DELTA `xor01` `acc_lenta` | **0.80–1.00** (umbral 0.80) | con 4 rasgos y 8 patrones el sistema deja de estar indeterminado; el humo da 0.625 en una semilla **con una clase sin morder** |
| RUIDO_DELTA `xor01` `acc_lenta` | 0.25–0.50 | humo: 0.250 |
| ORACULO_2C / ORACULO_2C_CTE `xor01` | 0.50–0.80, incierto | nadie lo ha corrido; es la pregunta secundaria |
| CUAD_DELTA `xor01` `acc_lenta` | ≈ 0.500 (réplica de 3d en semillas nuevas) | 3d: 0.500 [0.25, 0.81] |
| `px0` `acc_lenta`, todos los brazos | 0.90–1.00 | 3d: 1.000 en todos |
| `clases_sin_morder ≥ 1` | ~6 de 20 semillas | C: 3/10; 3d: 3/20 |

**Predicción cualitativa, comprometida:** **O1 pasa** → *el límite de XOR en v13 es de **selección de rasgos** (sesgo
inductivo), no de regla*: la regla local sí separa XOR cuando los rasgos son los correctos, y las tres refutaciones de
3b/3d estaban buscando en el sitio equivocado. Lo que **no** se podrá decir: que v13 aprende XOR — los rasgos se le
regalan; lo que queda abierto es **cómo se crean esos rasgos** (candidato ya escrito: el mecanismo 1 del informe, celdas
Kenyon conjuntivas / "unique cue", medible con `eta_s = 0` y K = 3 vs 5).
**Alternativa, si O1 cae** (ORACULO_DELTA < 0.80 o no supera al control): **la regla tampoco puede con 4 rasgos**, y
entonces el cuello no es ni la regla ni la dimensión sino **la dinámica**: el error `_ds = R − _ws` que sólo llega al
morder, el reparto de mordidas (82 % de una clase), la puerta, o la tasa efectiva `eta_s` frente a `lam_lenta`. Esa
sería la línea de 3f, con su preregistro y semillas nuevas — no una recalibración de éste.

## Refutación y qué NO se hará
- Si O1 cae, **no** se prueba otro `lam_lenta`, otro `eta_s` ni otro `clip_s` sobre estas semillas: se registra el número
  y se preregistra 3f. Nada se recalibra tras ver datos (regla 3).
- Si O1 pasa **sólo por el pareado** (mediana < 0.80 pero gana al control en ≥ 15/20), **O1 NO pasa**: hacen falta las
  dos mitades, y así queda escrito para que no se lea a medias.
- Si ORACULO_2C también llega a 0.80, se escribe que **la regla original nunca fue el problema** — sería una corrección
  del diagnóstico del bloque 3b, no un hallazgo nuevo de 3d/3e, y así debe registrarse.

## Las cuatro trampas (EQUIPO regla 5)
1. **Canal social simétrico:** no aplica (un solo organismo).
2. **Acierto sin balancear:** `acc`, `acc_lenta` y `ba` son balanceadas (el test de `xor01` es 8 comida / 4 veneno) y el
   empate exacto cuenta 0.5 — importa aquí porque con `oraculo01` **sin** constante (ORACULO_2C) la clase `(0,0)` vale
   exactamente 0 por álgebra (C): ese brazo arrastra 0.5 en 2 de sus 4 venenos por construcción, y por eso está
   ORACULO_2C_CTE al lado.
3. **Mundo que se come la comida:** sigue midiéndose por semilla (`clases_sin_morder`, mordidas pre-sonda por clase). No
   se toca el mundo en 3e: cambiarlo ahora mezclaría dos cambios.
4. **Sitios fijos que se memorizan:** los objetos reaparecen al azar y la sonda se calcula **antes** de que los patrones
   de test entren al mundo (`tipos.extend(test)` va después, en el mismo bloque).
   **Quinta, propia de 3e — la trampa del oráculo:** los rasgos se le REGALAN al organismo. `oraculo01` es información
   que v13 no construye por sí mismo; por eso el veredicto, si pasa, se escribe como *"el límite es de selección de
   rasgos"* y **nunca** como *"v13 resuelve XOR"*. El control RUIDO_DELTA existe justo para que "dar rasgos" no se
   confunda con "dar los rasgos buenos".
   **Sexta, medida y escrita: el control no es perfectamente inerte.** Con 3 de 6 píxeles activos por patrón, `P2·P3 = 1`
   en **2 de 4** patrones de la clase `00` (veneno), en **1 de 6** de `10` y de `01` (comida) y en **0 de 4** de `11`:
   un peso negativo en `P2·P3` ayuda algo en la clase `00`. RUIDO_DELTA puede por tanto quedar algo por encima de 0.5
   sin que eso invalide nada; lo que O1 exige es que ORACULO_DELTA lo supere pareado en ≥ 15/20.

## Humo de un proceso (corrido ANTES de fijar nada; `datos/xor_3e_humo_20260917_230742.{log,json}`, JSON `d687dfe9aa75344e`)
Un proceso, sin `Pool`: identidad + las dos corridas que pidió el coordinador (semilla 1, T = 100 000). Nada se ajustó.
- **Identidad 4/4** (`xor01`/`px0` × `lineal`/`cuadratica`, T = 60 000). **Inercia 16/16** contra el instrumento de 3d.
- **ORACULO_DELTA `xor01` s1: `acc_lenta` = 0.625** (`acc` 0.562). En **esa misma semilla**, el humo de 3d dio 0.312 con
  `cuadratica`: **el doble, con la misma regla y sólo cambiando los rasgos**. Sonda: `Ws(P0)` +1.02, `Ws(P1)` −0.39,
  `Ws(P0·P1)` −0.39, `Ws(cte)` −0.42.
- **RUIDO_DELTA `xor01` s1: `acc_lenta` = 0.250**, `Ws(P2·P3)` −0.25. El control se comporta como debe.
- La semilla 1 es de las **malas**: `{00: 48, 01: 0, 10: 204, 11: 15}` — la clase `01` sin una sola mordida antes de la
  sonda, y el marginal `Ws(P1)` sale negativo por eso. Que aun así suba a 0.625 es lo que hace esperar ≥ 0.80 en la
  mediana de 20 semillas, donde ~14 tendrán las cuatro clases.
- **`clip_s = 3.0` no aprieta:** `max|Ws|` 1.02 (oráculo) y 0.98 (ruido). Era un riesgo real —con 4 rasgos todo el error
  se concentra en pocos pesos y la solución exacta pediría `w0 = w1 = 4`, `w01 = −8`, `b = −3` (con `R = +1/−3`)— y no se
  materializó: el decaimiento deja el vector muy por debajo del tope. Se escribe para que el auditor lo verifique en la
  tabla (`max|Ws|` está en el log y en el JSON de cada brazo).

## Ejecución
**Lo corre el coordinador** (EQUIPO regla 3): `python experimentos/nivel7_xor_lectura/corre_xor_3e.py` (`--desde 61` por
defecto). Humo de un proceso: `--humo`. Sin `--rapido` (el gemelo compilado no tiene estos knobs).
