# PREREGISTRO — candidato **v15c**: la memoria de un golpe por pares, en la vía lenta del TRONCO

CREADOR A, 18-sep-2026. Lo corre el coordinador. **Los números de §7 (identidad y humo) están medidos; los de §4
(predicciones) NO.** Sin `Pool` por mi parte, sin commits.

## 1. De dónde viene

El bloque 3/3 cerró en 121–140: **M3 (memoria de un golpe por combinación de dos píxeles) da 1.000 registro y 1.000
estricta en los 12 nunca vistos, gana `(0,1)` en la sonda 20/20, `n\* = 7`**, con el rigging descartado (índice
1.000 = azar 1.000), `px0` 1.000 y `azar` 0.500. Registrado como **PRIOR ESTRUCTURAL de pares** (ERR-35): no es que
el organismo descubra la estructura — es que los candidatos *son* pares de píxeles, y ese prior rompe el empate de
**9 de 15 hipótesis con residuo 0** que hace indistinguible el mundo de 8 patrones.

Ese resultado vive en el **mundo de regla**, sobre un instrumento de experimento. Este preregistro pregunta lo
único que queda: **¿aguanta el TRONCO?**

## 2. Hipótesis

**H15c.** La memoria de pares puede entrar en la vía lenta de v14.1 **sin coste**: el examen del criterio v3', la
generalización y la retención se mantienen, y en el mundo de regla añade lo que el bloque 3 midió.

## 3. Instrumentos (todos por anclas; los congelados SÓLO se leyeron)

| archivo | origen | qué cambia |
|---|---|---|
| `organismo_v15c.py` | `organismo/organismo_v14.py` (TRONCO v14.1) | perilla `memoria_pares`; `None` ⇒ v14.1 **exacto** |
| `organismo_v15c_on.py` | `organismo_v15c.py` | la perilla fija en `'combi'` |
| `organismo_v15gc.py` / `_on.py` | `organismo/organismo_v14g.py` | ídem, mundo de regla |
| `bateria_v15c.py` | `organismo/bateria_v14.py` | sólo el módulo y los nombres de salida; **seis etapas y umbrales del criterio v3' INTACTOS** |
| `bateria_generaliza_v15c.py` | `organismo/bateria_generaliza.py` | **una** entrada nueva en `INSTRUMENTOS`; umbrales G1/G2/K intactos |

**La perilla, en una línea.** 15 celdas (los pares de píxeles) × 4 casillas (00/01/10/11), 15 contadores de visitas
y 15 errores propios (EMA de `(R − predicción)²`) = **135 números, sin pesos, sin tasa, sin tope**. En cada mordida
escriben las 15 celdas; **la primera vez que una celda ve una combinación escribe `R` de un golpe**. La vía lenta lee
la celda de menor error, con **abstención explícita (0.0)** en las combinaciones nunca vistas. **Desempate al azar
con el `rng` del organismo, y sólo se consume un número aleatorio cuando la perilla está ENCENDIDA y hay empate de
verdad** — por eso la identidad con la perilla apagada puede ser bit a bit.

## 4. Criterios (escritos antes)

- **V1 — examen del criterio v3', 8/8 en semillas 101–120**, con `bateria_v15c.py` (perilla **apagada**: es el
  criterio 5 del encargo, y comprueba que el instrumento no rompió nada).
- **V2 — generalización con la memoria ENCENDIDA**, `bateria_generaliza_v15c.py organismo_v15c_on 20 --desde 101`:
  **G1 ≥ 0.80, G2 ≥ 0.85, K 20/20**; y en el mundo de regla, semillas **121–140**: `xor01` **≥ 0.75 ESTRICTA**
  (abstención = fallo) y `px0` = **1.000**.
- **V3 — recuperación tras la inversión, no peor que v14.1.** Instrumento: el mundo largo
  (`experimentos/nivel8_mundo_largo/`) **sólo admite `mundo_largo`, que deriva de v13, no de v14/v15c**, y el runner
  de `nivel9_probar_si_mismo` tampoco toma un módulo por nombre. **Se declara NO MEDIBLE con los instrumentos de
  hoy**, y en su lugar se mide lo que sí existe en la batería: la **etapa E2 (inversión A↔B) del criterio v3'**, que
  V1 ya exige 20/20, **más** `invertir_en` en el mundo de regla con la perilla encendida (3 semillas, lectura).
  Si alguien construye el mundo largo sobre v15c, V3 se mide de verdad y este preregistro se enmienda.
- **V4 — capacidad y composición 3T-k sin cambio (±10 %).** `corre_3T_k.py` **no acepta un módulo por nombre**
  (comprobado) y `mundo_temporal_k` deriva de v13. **Se declara NO MEDIBLE sin construir el instrumento**; lo que sí
  se reporta, gratis, es `celdas` y `splits` de la batería de V1 contra los de v14.1 (si se separan más de ±10 %,
  es señal de que la memoria cambia el gasto de celdas aunque no toque la vía rápida).

## 5. Cláusula (la que pidió el coordinador)

**Si la memoria por pares daña la retención (V1 < 8/8) o la generalización (V2 fuera de umbral), NO entra al tronco:
queda como ÓRGANO DEL MUNDO DE REGLA**, igual que la tabla `M` del mapa y `gamma_soc`, y se registra así. No se
buscan valores intermedios en este preregistro.

## 6. Lo que NO se declara

Que v15c "resuelve XOR". Resuelve xor01 **con un prior de pares** y en un mundo de 6 píxeles donde la regla *es*
una función de dos de ellos. El prior no escala solo: para una regla de tres píxeles harían falta 20 tríos, y ese
es otro bloque. El control que separa prior de fuga sigue siendo **`azar` ∈ [0.35, 0.65]**, obligatorio en V2.

## 7. Medido ya — identidad y humo (NO es la serie)

`identidad_v15c.py` (un proceso, sin `Pool`, T = 30 000 salvo I2): **IDENTIDAD 32/32**.

| prueba | qué compara | resultado |
|---|---|---|
| **I1** | `v15c(memoria_pares=None)` ≡ `organismo/organismo_v14.py` (v14.1) | **24/24** (12 escenarios × 2 semillas: AB, inversión, patrón nuevo, `solap_AB=3`, sin plasticidad, vía lenta apagada, sin puerta, sin división, `mask_rel=0`, `puerta_pat=0`, las dos perillas v14 off, constantes v13) |
| **I2** | el `rng` **no se consume** con la perilla apagada (T = 120 000) | **2/2** |
| **I3** | `v15gc(None)` ≡ `organismo/organismo_v14g.py` (px0, xor01, azar) | **6/6** |
| **I4** | `v15gc('combi')` contra `organismo_g3A('combi')` | **la equivalencia exacta NO existe y no se reclama** — v15gc lleva la hija dispersa y la puerta por código de v14.1 (g3A no) y g3A lleva la vía lenta cuadrática (v14.1 no). Lo que sí debe coincidir, la **celda ganadora**, coincide: **(0,1) en 3/3**, cobertura **4/4**, 60 casillas vistas |

**Humo** (`corre_v15c.py --humo`, un proceso, sin `Pool`; `datos/v15c_humo_20260918_075004`, `7e94d7ff5a86d2b9`;
159 s): mundo de regla, semilla 121, T = 200 000, memoria ON contra OFF **pareado**:

| regla | memoria | registro | ESTRICTA | ba | ganadora | cobertura | celdas | muertes |
|---|---|---|---|---|---|---|---|---|
| xor01 | **combi** | **1.000** | **1.000** | 0.984 | **(0,1)** | 4/4 | 73 | 249 |
| xor01 | — | 0.375 | 0.375 | 0.551 | — | — | 70 | 244 |
| **px0** | **combi** | **0.800** | **0.800** | 0.707 | (0,1) | 4/4 | 54 | 285 |
| **px0** | — | **0.900** | 0.900 | 0.839 | — | — | 62 | 269 |
| azar | combi | 0.500 | 0.500 | 0.405 | (1,3) | 4/4 | 61 | 292 |
| azar | — | 0.400 | 0.400 | 0.510 | — | — | 59 | 244 |

**AVISO, y es el que importa: con una semilla, la memoria SUBE xor01 (0.375 → 1.000) y BAJA px0 (0.900 → 0.800).**
No es sorprendente al mirar el mecanismo: la perilla **sustituye** la lectura lineal de la vía lenta por la tabla de
pares, y `px0` es una regla lineal de **un** píxel — una tabla sobre pares la lee peor. V2b exige `px0` = **1.000**,
así que **este humo ya apunta a que V2b puede caer y a que se aplique la cláusula §5** (órgano del mundo de regla, no
tronco). **No cambio el criterio**: se corre como está escrito y, si cae, cae. La variante obvia —que la vía lenta
**sume** la lectura lineal y la memoria en vez de sustituirla, o que enrute según cuál de las dos tiene menos error—
es **otro mecanismo** y va en un preregistro nuevo, no en una enmienda después de ver estos números.
Las muertes suben un poco con la memoria (249/285/292 contra 244/269/244): se reporta pareado en la serie.

## 8. Coste

V1: 20 semillas × las seis etapas (`bateria_v15c.py 20 --log`) ≈ 15–20 min con `Pool(14)`.
V2: `bateria_generaliza_v15c.py organismo_v15c_on 20 --desde 101 --log` ≈ 5–8 min, más 40 corridas del mundo de
regla (xor01 y px0, 121–140) ≈ 2 min. Identidad: ~4 min en un proceso.
