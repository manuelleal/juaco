# PREREGISTRO — candidato **v15d**: la memoria de pares **suma o enruta**, no sustituye

CREADOR A, 18-sep-2026. Lo corre el coordinador. **Los números de §7 están medidos; los de §4 NO.** Sin `Pool` por
mi parte, sin commits.

## 1. De dónde viene: v15c cayó, y cayó donde estaba escrito

v15c llevó la memoria de un golpe por pares a la vía lenta **sustituyendo** la lectura lineal. Resultado registrado:
**V2a G1 0.500 / G2 0.513** (v14.1: G1 ≥ 0.80 / G2 ≥ 0.85) — **rompe la generalización lineal del tronco** — mientras
**V2b xor01 0.812 estricta** contra 0.438 sin memoria. La cláusula se aplicó: no entra al tronco, queda como órgano
del mundo de regla. El humo de una semilla ya lo había avisado (px0 0.900 → 0.800) y el diagnóstico estaba escrito
antes de la serie: **una tabla sobre PARES no puede leer una regla lineal de UN píxel.**

**v15d corrige exactamente eso: la lineal no se pierde.**

Dos defectos de v15c que arreglo aquí y declaro:
1. **El examen midió la perilla APAGADA.** `bateria_v15c` apuntaba a `organismo_v15c` (OFF), así que V1 no medía al
   candidato. `bateria_v15d` apunta a **`organismo_v15d_on`**.
2. **Colisión de nombre `_ev`** (hallada por mí al construir v15d): mi variable local del bucle pisaba la función
   `_ev(_k)` de v14.1 (la evidencia que lee la puerta por código). **Con `puerta_pat > 0` y la perilla ENCENDIDA,
   `organismo_v15c` lanzaba `TypeError: 'float' object is not callable`.** No saltó en la serie porque V1 corrió con
   la perilla apagada y V2a/V2b usaron el mundo de regla con `puerta_pat` en su valor por defecto. **Arreglado en
   los dos constructores (`_ev` → `_erv`) y verificado con `puerta_pat=5`.** Si el coordinador quiere reusar los
   números de V2a de v15c, conviene comprobar que su log no trae excepciones.

## 2. Hipótesis

**H15d.** La memoria de pares entra en la vía lenta **sin costar la generalización lineal** si no sustituye a la
lectura lineal: `'suma'` (las dos se suman) o `'ruta'` (se usa la de menor error propio).

## 3. Instrumentos (por anclas; los congelados SÓLO se leen)

`organismo_v15d.py` ← `organismo/organismo_v14.py` (v14.1) · `organismo_v15d_on.py` (perilla fija `'suma'`) ·
`organismo_v15gd.py` / `_on.py` ← `organismo/organismo_v14g.py` · `bateria_v15d.py` ← `organismo/bateria_v14.py`
**sobre `organismo_v15d_on`** · `bateria_generaliza_v15d.py` ← `organismo/bateria_generaliza.py` (una entrada nueva;
umbrales G1/G2/K intactos).

**Perilla `memoria_pares = None | 'suma' | 'ruta'`.** Estado: 15 celdas (pares) × 4 casillas + 15 visitas + 15
errores propios + **1 error propio de la lineal** = **136 números**.
`'suma'` → `lineal(P) + tabla(P)`, con **abstención** de la tabla (0.0) en combinaciones nunca vistas.
`'ruta'` → `lineal(P)` si `err_lineal ≤ err_celda_ganadora`, si no `tabla(P)`.
`None` → la línea literal de v14.1; **no se evalúa nada nuevo y no se toca el `rng`**.
Desempate de la celda ganadora **al azar con el `rng` del organismo**, y sólo se consume un número cuando la perilla
está ENCENDIDA y hay empate de verdad.

## 4. Criterios (escritos antes de la serie)

- **V1 — examen del criterio v3', 8/8 en semillas 101–120, CON LA PERILLA ENCENDIDA** (`bateria_v15d.py`, que apunta
  a `organismo_v15d_on`). Corrige el defecto de v15c.
- **V2a — generalización con la perilla ON:** `bateria_generaliza_v15d.py organismo_v15d_on 20 --desde 101` →
  **G1 ≥ 0.80, G2 ≥ 0.85, K 20/20**. *Éste es el criterio que mató a v15c (0.500 / 0.513).*
- **V2b — mundo de regla, semillas 121–140, los tres modos pareados:** `xor01` **ESTRICTA ≥ 0.75**; `px0` **≥ el de
  la perilla apagada en el mismo mundo y las mismas semillas** (no 1.000: el umbral de v15c estaba mal puesto y el
  propio v14.1 da 0.900 ahí); `azar` ∈ **[0.35, 0.65]**.
- **V3 — `n\*` como número principal:** primer número de encuentros con mediana ≥ 0.75 en xor01, por modo.
- **V4 — coste:** `celdas` y `splits` dentro de ±10 % de la perilla apagada, y muertes pareadas.

## 5. Predicción numérica mía (para poder equivocarme)

- `'suma'`: **V2a pasa** (G1 ≥ 0.80, G2 ≥ 0.85) — la lineal sigue entera y la tabla sólo añade — y **V2b xor01
  estricta ≥ 0.75**. Es el modo que apuesto.
- `'ruta'`: **V2a también pasa**, porque en `px0` la lineal tiene menos error y gana el ruteo; pero **predigo que en
  `xor01` queda por debajo de `'suma'`**, porque el ruteo es una decisión dura tomada con una EMA ruidosa.
- `px0` con `'suma'`: **igual o mejor** que la perilla apagada (la tabla abstiene o aporta poco); si baja, mi
  diagnóstico del fallo de v15c estaba incompleto.
- `n\*` para xor01: **≤ 20** con `'suma'`.

## 6. Refutación y cláusula

- **H15d se refuta** si `'suma'` falla V2a (es decir: si sumar también rompe la generalización lineal). Entonces el
  problema no era sustituir sino **tener** la tabla, y la memoria de pares se queda definitivamente como órgano del
  mundo de regla.
- Si `'suma'` pasa V2a pero falla V2b, la memoria no aporta en el tronco: se reporta y no entra.
- **No se buscan modos intermedios después de ver los datos.** `'suma'` y `'ruta'` quedan fijados aquí.

## 7. Medido ya (identidad y humo) — NO es la serie

**Identidad: 32/32** (`identidad_v15d.py`, un proceso, T = 20 000 salvo I2). I1 `v15d(None)` ≡ v14.1 en **24/24**
(12 escenarios × 2 semillas) · I2 **el `rng` no se consume con la perilla apagada** (T = 120 000, 2/2) ·
I3 `v15gd(None)` ≡ `v14g` **6/6**. La colisión `_ev` está arreglada y verificada con `puerta_pat=5`, en v15d **y**
en v15c.

**I4 — px0, la regla lineal que v15c rompió** (3 semillas, T = 100 000; NO es identidad):

| semilla | v15c *sustituye* | **v15d `'suma'`** | v15d `'ruta'` | v14.1 (perilla off) |
|---|---|---|---|---|
| 1 | 0.700 | **1.000** | 0.700 | 1.000 |
| 2 | 0.900 | **1.000** | 0.900 | 0.800 |
| 3 | 0.800 | **1.000** | 0.800 | 1.000 |

**`'suma'` da 1.000 en 3/3; `'ruta'` se comporta igual que sustituir.** Es la señal que predice §5.

**Humo** (`corre_v15d.py --humo`; `datos/v15d_humo_20260918_082138`, `5cd151d812eba2e1`; 190 s, un proceso, semilla
121, T = 200 000, los tres modos **pareados**):

| regla | modo | registro | ESTRICTA | ba | ganadora | celdas | muertes |
|---|---|---|---|---|---|---|---|
| xor01 | **suma** | **0.875** | **0.875** | 0.878 | (0,1) | 68 | 233 |
| xor01 | ruta | 0.875 | 0.875 | 0.892 | (0,1) | 69 | 224 |
| xor01 | — | 0.375 | 0.375 | 0.551 | — | 70 | 244 |
| px0 | **suma** | **1.000** | **1.000** | 0.999 | (0,1) | **33** | 285 |
| px0 | ruta | 0.900 | 0.900 | 0.865 | (0,4) | 63 | 257 |
| px0 | — | 0.900 | 0.900 | 0.839 | — | 62 | 269 |
| azar | suma | **0.700** | 0.700 | 0.600 | (3,4) | 65 | 303 |
| azar | ruta | 0.500 | 0.500 | 0.405 | (1,3) | 61 | 292 |
| azar | — | 0.400 | 0.400 | 0.510 | — | 59 | 244 |

**Dos avisos que dejo escritos antes de la serie.** (1) `azar` con `'suma'` sale **0.700**, fuera de la banda
[0.35, 0.65] del control V2b. Con una semilla no decide nada, pero **es el control que separa prior de fuga** y si
en 20 semillas se queda fuera, v15d **no entra** aunque V1 y V2a pasen. (2) `px0` con `'suma'` usa **33 celdas
contra 62** de la perilla apagada (3 divisiones contra 32): es un cambio grande en el gasto de la vía rápida, y V4
lo mide con ±10 % — **probablemente lo incumpla**. Lo anoto ahora, no después.

## 8. Coste

V1 `bateria_v15d.py 20 --desde 101 --log` ≈ 15–20 min con `Pool(14)` · V2a `bateria_generaliza_v15d.py
organismo_v15d_on 20 --desde 101 --log` ≈ 5–8 min · V2b 180 corridas del mundo de regla (3 modos × 3 reglas × 20
semillas) ≈ 4–5 min. Identidad ~2 min en un proceso. El runner lanza las baterías como **subprocesos secuenciales**:
nunca dos `Pool` a la vez.
