# Nivel 7 (composición) — **HIJA DISPERSA**: ¿la hija de v11 debe nacer ciega a parte del patrón, y no sólo fuera de él?

**Escrito ANTES de correr, 18 sep 2026.** Propuesta B-1 del creador B (`registro/investigacion/PUENTE_creacion.md`,
sección "Propuestas para el coordinador"). Regla 12. El instrumento ya existe y su identidad con las perillas apagadas
está verificada; los números de abajo son los de la propuesta, **sin tocar**, y los de la mini-prueba están declarados
como lo que son: 3 semillas (1–3), humo, no confirmatorio.

## 0. Qué se sabe, y qué corrige este bloque

- 3T-k replicado: **compone hasta 3 pasos**; a k = 4 y 5 la separación sobrevive (`sep` ≥ 1.9, 20/20 pareado) pero la
  ventaja conductual del último cuarto queda al filo (`lift_q4` 0.152 / 0.140 en k = 4 y 0.144 / 0.133 en k = 5) con el
  pool de celdas agotándose (78–90/90). La lectura registrada fue: *el techo es el presupuesto de celdas*.
- **Medido por el creador B (mini-prueba, k = 5, semillas 1–3, T = 100 000): el pool NO es el techo.** Con `nkmax = 180`
  el organismo usa 101/99/94 celdas —nunca las 180— y `lift_q4` sale 0.159/0.059/0.099 contra 0.150/0.048/0.112 con 90:
  **duplicar el pool no devuelve nada**. Además, de las 90 celdas activas, **51/46/55 tienen |Wp−Wn| ≤ 0.2** (no llevan
  valor legible) y **24 nunca entraron en un código mordido**; el pool se agota en el último tercio (`t_pool`
  67 853 / 91 200 / 93 092) y sólo bloquea **3/7/2 divisiones**.
- Hipótesis que este bloque prueba: lo que se agota no son las celdas sino la **evidencia por código**. A profundidad k
  hay 2^(k−1) rellenos distractores; el código de v13 es exacto por patrón compuesto, así que cada código recibe
  ~1/2^(k−1) de las mordidas, y **cada hija, que ve TODO el patrón compuesto, cubre un solo relleno**: el conflicto de
  la madre se reabre con el siguiente relleno y la fisión vuelve a borrar valor. Una hija ciega a parte de `P` cubre
  una **familia** de rellenos, cierra el conflicto y compone con menos celdas.
- **Contraste con v12 (refutada):** v12 hacía la hija **menos** ciega hacia AFUERA de `P` (ceguera graduada). Esto es
  la dirección contraria: ceguera **parcial hacia ADENTRO** de `P`.

## 1. Mundo e instrumento

- Mundo: `mundo_temporal_k` sin cambios (3T con profundidad k; la regla depende del slot **más profundo**, los
  intermedios son distractores). **El mundo no cambia en este bloque: cambia UNA línea del organismo.**
- Instrumento: `experimentos/nivel7_hija_dispersa/mundo_hija_dispersa.py` (`d305d53186fcbcd6`), construido POR ANCLAS
  con `construye_hija_dispersa.py` (`fd82df7186ce8151`) desde `experimentos/nivel7_3T_k/mundo_temporal_k.py`
  (`68736baafe7c8cdb`), que sólo se lee. La cadena de constructores de la que se funde (creador B, scratch) es
  `experimentos/creacion_B/construye_B1.py` → `mundo_k_B.py` (`c123df80b77062d9`) → `construye_B2.py` →
  `mundo_k_B2.py` (`e7f8d22b599a8f16`) → `construye_B3.py` → `mundo_k_B3.py` (`1214d15e210237b6`); el constructor
  consolidado comprueba que el cuerpo generado es **byte a byte** el de `mundo_k_B3.py`.
- **Identidad obligatoria** (`identidad_hija_dispersa.py`, y repetida dentro del runner antes de nada): con
  `recic=0, mask_rel=0, n_cf=1` el instrumento es `mundo_temporal_k` **bit a bit**, todas las claves. Ya verificada
  7/7 en la cadena del creador B (C3 k=1 · C3 k=4 · C3C k=4 · C1p k=1 · C3 k=5 T=100k). **Si el runner no obtiene
  3/3 en su etapa de identidad, aborta.**

## 2. El mecanismo (regla local, y qué memoria exige)

Una línea del nacimiento de v11: `kj = clip(KW[c]·0.95 + paso·dist, 0, 5) · rel`, con `rel ⊊ (P>0)` en vez de
`rel = (P>0)`.

| brazo | `mask_rel` | `n_cf` | qué es | memoria nueva |
|---|---|---|---|---|
| **V13** | 0 | 1 | el tronco tal cual (control de inercia) | — |
| **REL** (a) | 2 | 1 | `rel[i] ⟺ P[i]>0 ∧ ( \|m̂p[i]−m̂n[i]\| > δ_s ∨ min(m̂p[i],m̂n[i]) > 1−δ_c )` | 2 vectores `NIN` + 2 escalares **por celda** |
| **RELD** (a+dif) | 2 | 4 | lo mismo, dividiendo sólo tras 4 conflictos | + 1 entero por celda |
| **AZAR** (b) | 4 | 1 | **control**: subconjunto AL AZAR de `(P>0)` de la misma cardinalidad | **cero** |
| **SLOT** (c) | 3 | 1 | **control**: la misma máscara de (a) con el bloque del slot profundo intercambiado con el de un distractor (intercambio forzado) | igual que (a) |

`m̂p = mup[c]/zp[c]` y `m̂n = mun[c]/zn[c]` son las medias de `P` **condicionadas al signo de R**, EMA con normalizador
(`ema_c = 0.05`). Dos ramas dendríticas: **contexto** (lo presente en las dos clases) Y **discriminador** (lo que
separa las clases). Umbrales `δ_s = δ_c = 0.25`, **fijados antes de correr** y no barridos: la separación medida entre
el slot causal y los distractores es de un factor ~8 (`max|m̂p−m̂n|` por slot a k=5: s0 0.00 · s1 0.13 · s2 0.09 ·
s3 0.09 · s4 0.12 · **s5 1.00**), así que cualquier umbral en [0.2, 0.9] da la misma máscara.
Los controles (b) y (c) sortean con un **RNG aparte** (`seed + 200000`) que no toca el flujo de azar del organismo.
La perilla `recic` (reciclaje de celdas) queda **en 0** en todos los brazos: el creador B la refutó antes de
preregistrarla (sólo compraría 2–7 divisiones en 100 000 pasos).

## 3. Diseño

- Brazos: **V13 · REL · RELD · AZAR · SLOT**, cada uno en **C3** (la pregunta) y **C3C** (canal temporal falso: control
  de artefacto de siempre). `k ∈ {4, 5}`, `T = 100000`, semillas **61–80**; réplica en **81–100** con `--desde 81`
  si pasa. Más `k = 1` sólo con REL en C3 (control de inercia del mecanismo, ver P4).
- Total: 5 brazos × 2 escenarios × 2 k × 20 semillas + 20 (k=1) = **420 corridas** + 6 de identidad.
- Configuración de v13 en todos los brazos: `mu_norm=True, div_signo=True, eta_s=0.015, puerta=3`.
- Comparaciones **pareadas semilla a semilla**; se reportan medianas y rangos (regla 6), nunca sólo la media.

## 4. Predicciones numéricas (las de la propuesta B-1, sin tocar)

- **P1 (celdas).** `celdas(REL) ≤ 0.75 × celdas(V13)` en **≥ 18/20** a **k = 5**, y `≤ 0.85 ×` en **≥ 18/20** a **k = 4**.
- **P2 (conducta).** `lift_q4(REL)` **mediana ≥ 0.18** a k = 5, y `> lift_q4(V13)` en **≥ 15/20** pareado.
- **P3 (representación).** `sep(REL)` **mediana ≥ 2.2** y `sep(REL, C3) − sep(REL, C3C) ≥ 1.0` en **≥ 18/20**.
- **P4 (inercia).** A **k = 1** el brazo REL es **idéntico a V13 semilla a semilla** (todas las claves comparadas):
  donde no hay nada irrelevante que ignorar, la máscara no hace nada. Ya observado 3/3 en la mini-prueba.
- **Controles de siempre:** C3C de cada brazo con `sep < 1.0` y `lift_q4 < 0.15` (si el canal falso compone, hay
  artefacto y se para).

## 5. Controles que pueden fallar, y sus cláusulas (escritas antes)

- **R1 — refutación del mecanismo entero.** Si **REL no cumple P1 a k = 5**, el ahorro de celdas —lo único que salió
  3/3 en la mini-prueba— no replica y la propuesta cae. No se reajusta ningún umbral: se registra y se cierra.
- **R2 — refutación como mecanismo de composición.** Si **ni REL ni AZAR cumplen P2 a k = 5**, la hija dispersa no
  compone mejor: se declara sólo como **economía de celdas** (con su número) y **no toca el tronco**.
- **R3 — degradación a "dispersión" (el control que casi la tumba ya).** Si **REL no supera a AZAR en `lift_q4` en
  ≥ 14/20 pareado**, lo que actúa es la **dispersión del campo receptivo de la hija** y no la relevancia: se declara
  **"hija dispersa"** (una línea, memoria cero) y la traza condicionada `m̂p/m̂n` queda como **hallazgo de
  representación**, no como órgano; la variante que iría al tronco sería **AZAR**, la barata. *En la mini-prueba AZAR
  llegó a 0.208 contra 0.221 de REL: con 3 semillas no se distinguen, así que esta cláusula es la más probable.*
- **R4 — artefacto de instrumento.** Si **SLOT supera a REL en ≥ 14/20 pareado**, la máscara con el slot **equivocado**
  sería mejor que la correcta: eso no es un mecanismo, es un artefacto. Se abre ERR, se para el bloque y se audita el
  instrumento antes de cualquier lectura.
- **Vocabulario permitido según el resultado.** Si pasan P1–P3 y REL > AZAR: *"la hija que nace ciega a lo irrelevante
  compone historias más profundas con menos celdas"*. Si pasa R3: *"la hija que nace con un campo receptivo más
  disperso compone historias más profundas con menos celdas; qué píxeles conserva no importa"*. Si pasa R2: *"gasta la
  mitad de las celdas para la misma composición"*. En ningún caso "aprende a ignorar", "atiende" ni "selecciona".

## 6. Antes de que esto toque el tronco (no es parte de este bloque)

`bateria_v13.py` 8/8 y `bateria_generaliza.py` G1 ≥ 0.80 / G2 ≥ 0.85 sobre un `organismo_v13` con la misma perilla,
en las semillas que esas baterías usan (ERR-20). Este bloque mide **composición y presupuesto**, no retención ni
generalización: el mecanismo vive aquí en la copia del mundo, no en el tronco.

## 7. Mini-prueba que originó la propuesta (3 semillas, humo, NO confirmatorio)

Semillas 1–3, C3, T = 100 000, v13 = `mu_norm/div_signo/eta_s=0.015/puerta=3`. Medianas, y entre paréntesis las tres.

| k | brazo | `lift_q4` | `sep` | celdas |
|---|---|---|---|---|
| 5 | V13 | 0.112 (0.150/0.048/0.112) | 1.99 | 90/90/90 |
| 5 | V13 con `nkmax`=180 (control del pool) | 0.099 (0.159/0.059/0.099) | 1.51 | 101/99/94 |
| 5 | **REL (a)** | **0.195** (0.386/0.144/0.195) | 2.87 | **36/75/65** |
| 5 | **RELD (a)+diferida** | **0.221** (0.210/0.221/0.388) | 2.70 | **33/52/56** |
| 5 | AZAR (b) | 0.208 (0.206/0.264/0.208) | 2.00 | 74/55/78 |
| 5 | SLOT (c) | 0.158 (0.373/0.158/0.151) | 2.05 | 43/82/67 |
| 5 | sólo diferida, sin máscara | 0.133 (0.117/0.133/0.152) | 1.61 | 88/85/82 |
| 4 | V13 | 0.236 (0.201/0.300/0.236) | 2.31 | 70/36/86 |
| 4 | REL (a) | 0.175 (0.143/0.380/0.175) | 2.39 | 39/35/81 |
| 4 | AZAR (b) | 0.221 (0.221/0.221/0.198) | 2.58 | 62/83/64 |
| 1 | V13 y REL | 0.366 / 0.366 — **idénticos** | 3.94 | 35/35/36 |

Gana a V13 en `lift_q4` en 3/3 a k = 5 y baja celdas en 3/3 a k = 4 y k = 5; **no** gana a k = 4 en conducta (1/3).
La varianza entre semillas es enorme (0.14–0.39): con n = 3 **lo único robusto es el ahorro de celdas**, y por eso
P1 es la predicción cuyo fallo (R1) tumba el bloque.
