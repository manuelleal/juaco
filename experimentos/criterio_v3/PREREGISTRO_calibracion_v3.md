# PREREGISTRO — bloque A-CAL: "el criterio se calibra contra su propio placebo" (criterio v3, ERR-91)

**Escrito ANTES de correr nada** (21 sep 2026, 19:0x). Carpeta `experimentos/criterio_v3/`. Letra que se calibra:
`registro/CRITERIO_TRONCO_v3.md` (escrita también antes). Umbrales en `umbrales_v3.py`, importado por el runner (ERR-31):
este documento y ese módulo dicen lo mismo, y ninguno se toca después de correr.

---

## 1. Hipótesis

*Un criterio de tronco sólo es un instrumento si (a) deja pasar a un **placebo** —un candidato cuya ley es exactamente la
del tronco— con probabilidad ≥ 0.90, y (b) rechaza con probabilidad ≥ 0.95 a un candidato peor que el **margen que el
propio criterio declara**. El criterio v2 falla (a): reconstruido sobre corridas reales, el placebo pasa T-A con 0.316 y
T-A ∧ T-C (ii) con 0.006. La letra v3 (no inferioridad con el margen ya declarado, sin umbrales sobre el nulo) cumple las
dos.*

Esto no mide un órgano. Mide el instrumento que decide qué órgano entra. Por eso el "candidato" de este bloque es el
tronco mismo.

## 2. Mecanismo mínimo y memoria nueva: **CERO**

No se toca el organismo. Se añade **una perilla de instrumento**, `placebo = k`: consume `k` sorteos del mismo generador
por paso y **descarta el valor**; ninguna decisión los mira. Misma ley, otra trayectoria. Es la definición operativa de
"candidato indistinguible del tronco".

- Sin arrays, sin contadores, sin estado: una línea (`for _ in range(placebo): rng.random()`) como **primera sentencia
  del bucle**, antes de cualquier decisión. `placebo = 0` ≡ tronco **bit a bit**.
- El brazo **PEOR** no necesita perilla nueva: usa `costo` y `costo_a`, que **ya son argumentos del tronco** (el coste de
  vida del mundo vivo, 0.001 en `mini_vivo.CUERPO`). PEOR = el mismo organismo con coste de vida mayor.

## 3. Instrumento y anclas

| archivo (todos en `experimentos/criterio_v3/`) | qué es | origen y sha del origen |
|---|---|---|
| `construye_criterio_v3.py` | constructor por anclas, no corre nada; aborta si un origen cambia | — |
| `organismo_v3cal.py` | el instrumento | `nivel11_mundo_vivo/organismo_vivo_rep2.py` **96feb4918dc5d694** (cadena `organismo_vivo_rep` aa823d56c2d4213c ← `organismo_vivo` 20c0961c79de8825 ← `organismo/organismo_v14.py` feefc88b1fd8d434) + B-5 `desambiguar` (texto **literal** de `creacion_B/construye_codigo.py`, por defecto 1 = TRONCO v14.2 **17528d767fcebaf6**) + `invertir_vivo_en` (texto de `construye_v15_dE5.py`) + **`placebo`** |
| `identidad_criterio_v3.py` | arnés, un proceso, escribe su JSON | — |
| `umbrales_v3.py` | la letra v2, la letra v3 y CAL-1..CAL-5 (ERR-31) | `CRITERIO_TRONCO_v2.md`, `CRITERIO_TRONCO_v3.md` |
| `regla14_campo_a_campo.py` | regla 14 adaptada (ver §7) | `corre_vivo_rep2.BRAZOS`, `mini_vivo.BRAZOS` |
| `corre_criterio_v3.py` | runner de seis etapas, `--humo` de un proceso | por anclas desde `tronco_v15_dE5/corre_dE5_v2.py` |
| `prueba_wiring.py` | prueba de cableado con crudos **sintéticos**: no corre ninguna simulación, no abre Pool, no escribe en `datos/`; evita que la serie se caiga en la etapa 6 tras quince minutos de Pool | — |

**Arnés de identidad (obligatorio antes de mirar números).** I1 `placebo=0, vivo=0, n_nec=1` ≡ `organismo_v142` bit a bit
en los 9 escenarios de `bateria_v142.ETAPAS` × 3 semillas · I2 `placebo=0, desambiguar=0` ≡ `organismo_vivo_rep2` en 3
montajes × 2 semillas · I3 B-5 inerte en los mundos del tronco · I4 `placebo=0` ≡ no pasar la perilla · I5
`invertir_vivo_en > T` inerte · I6 lectura (no puerta) del rango de muertes con `placebo=1`.
**Controles que DEBEN fallar:** M1 `placebo=1 ≠ placebo=0` (mundo vivo) · M2 `placebo=2 ≠ placebo=1` · M3
`placebo=1 ≠ 0` también en el mundo del examen · M4 el brazo PEOR sí cambia · M5 `invertir_vivo_en = T/2` sí cambia ·
M6 paja del comparador · M7 `desambiguar=1 ≠ 0` en una semilla ALIAS.

## 4. Diseño de la serie

Tres brazos del **mismo** organismo, en las mismas semillas: **OFF** (`placebo=0` = tronco v14.2), **PLACEBO**
(`placebo=1`), **PEOR** (`costo = costo_a = 0.001 × m`, `m` en §6/§10). Cada puerta se juzga con **la letra v2 y la letra
v3 lado a lado, sobre los mismos números**.

- **T-A**: `corre_vivo_rep2`, brazos `VIVO` y `CUELLO_MIN`, T = 100 000, **n = 40** por brazo.
- **T-C (ii)**: `mini_vivo` brazo `VIVO` con `invertir_vivo_en = 50 000`, T = 100 000, **n = 40**.
- **Calibración (etapa 6)**: las 80 corridas del **nulo** de cada brazo (40 OFF + 40 PLACEBO, misma ley) se reparten al
  azar en dos brazos de n y se aplica cada letra; B = 4 000 repartos. Da P(pasa) bajo el nulo para n = 20 y n = 40, con v2
  y con v3. **CAL-3a**: el mismo reparto restando **δ = −20** a `r` (o a `rev`) del brazo candidato: el desplazamiento
  exacto, sin CPU y sin calibrar nada.

**Semillas NUEVAS** (verificadas libres con `grep -rnE '\b2[0-4][0-9]{2}\b'` sobre `registro/`, `experimentos/`,
`organismo/` y con búsqueda en los JSON de `datos/`, el 21-sep 19:00; se declaran las ocupadas):

| uso | semillas | por qué |
|---|---|---|
| T-C (ii) | **2121–2160** (40) | el rango 2141–2160 que pidió el encargo es su segunda mitad; 2121–2140 está libre |
| T-A | **2161–2200** (40) | exactamente lo pedido |
| réplica T-A | **2281–2320** (40) | **2201–2240 NO se usa**: el creador C reservó **2201–2280** para dE5-fam |
| réplica T-C (ii) | **2321–2360** (40) | libre |

Ocupadas y evitadas: **2001–2080** (dE5-v2 y v15f-v2), **2101–2120** (tercera serie de BA-v, lanzada hoy),
**2201–2280** (reserva de C). Ningún JSON de `datos/` usa semillas ≥ 2100 a esta hora.

## 5. Predicción numérica (con rango) — firmada antes de correr

| id | qué | predicción |
|---|---|---|
| **CAL-1** | el PLACEBO pasa **T-A v3** (n = 40, margen 10), por reparto del nulo | **0.90–0.98** |
| **CAL-2** | el PLACEBO pasa **T-A v2** (n = 20, con `A₁₂ ≥ 0.50`) | **0.25–0.40** (reconstruido por A: 0.316) |
| **CAL-3** | v3 rechaza un candidato desplazado **δ = −20** puntos de `r` (y de `rev`) | pasa **≤ 0.05** |
| **CAL-4** | marginales PLACEBO vs tronco: `A₁₂` **NO pareado** en las 6 comparaciones (`r` y muertes en VIVO y CUELLO_MIN, `rev` y muertes en la reversión) | todas en **[0.40, 0.60]** |
| **CAL-5** | el PLACEBO pasa **T-C (ii) v2** (`A₁₂ ≥ 0.75`, n = 20) | **0.01–0.05** |

Predicciones de acompañamiento (se reportan, no son puertas): el PLACEBO **pasa** T-A v3 y T-C (ii) v3 en la realización
única de la serie; el brazo PEOR **cae** en las dos letras; `Δr(PEOR)` en la serie ≤ −20 (si `|Δr| < 20`, se declara que
el brazo PEOR resultó más suave de lo pedido y CAL-3 se lee sólo de CAL-3a).

## 6. Control que puede fallar, y qué refuta el bloque

**El control que puede fallar es CAL-4.** Si consumir un sorteo por paso **cambia la ley** (por ejemplo porque el número
de sorteos que el organismo gasta depende del estado y el desplazamiento desincroniza algo sistemáticamente), el placebo
no es placebo y **el bloque entero se anula**: no se lee ninguna otra línea. Plan B ya validado y sin CPU: el placebo por
reparto de corridas reales del tronco (§8 del análisis de A).

**Qué refuta la hipótesis del bloque:**
1. Si el placebo pasa **T-A v2** en ≥ 0.85 de los repartos → el diagnóstico de ERR-91 es falso y **v2 se queda**.
2. Si **v3** deja pasar δ = −20 en > 0.10 → v3 es demasiado laxa, **se retira** y se escribe v4 con ERR.
3. Si **CAL-4** sale fuera de [0.40, 0.60] en cualquiera de las 6 → instrumento roto, no se lee nada.
4. Si el placebo **cae** T-A v3 en la realización única *y* el reparto da ≥ 0.90 → es mala suerte declarada, se reporta y
   se corre la réplica; si cae también en la réplica, v3 no cumple (a) y se retira.

**Regla del brazo PEOR, escrita antes del humo (para no recalibrar después):** `m` = el **menor** de {1.25, 1.50} cuyo
`Δr` en la semilla de humo sea ≤ −20; si ninguno llega a −20, `m = 1.50` **y se declara que el brazo PEOR es más suave que
el desplazamiento pedido**. Se fija **una vez**, en el humo, se escribe en §10 y en `umbrales_v3.PEOR['m']`, y no se
vuelve a tocar. (Precedente: `C_CONST` de `PREREGISTRO_dE5_v2.md` §10.)

## 7. Regla 14, y las cuatro trampas

**Regla 14 adaptada y declarada.** A-CAL **no copia ninguna batería** (no corre T-B ni el examen): importa
`corre_vivo_rep2.BRAZOS` y `mini_vivo.BRAZOS` sin copiarlos. Por eso la regla 14 se aplica a lo único que sí se escribe
aquí: **los kwargs que el runner pasa**. `regla14_campo_a_campo.py` verifica, campo a campo, que cada brazo sea el
montaje del tronco **más exactamente** los campos declarados (`desambiguar=1`, `placebo`, `invertir_vivo_en`; y para
PEOR, `costo`/`costo_a` con el factor declarado), que PLACEBO difiera de OFF **sólo** en `placebo`, y que PEOR difiera de
OFF **sólo** en el coste de vida.

**Las cuatro trampas.**
1. *Canal simétrico*: no hay canal ni emisor/receptor en este bloque. No aplica.
2. *Acierto sin balancear*: **es la trampa central del bloque**, y v3 la prohíbe explícitamente (regla 5 de §2: toda tasa
   con su par y con J). A-CAL no reporta ninguna tasa de acierto: reporta `r`, muertes y `rev`, que son conteos con signo.
3. *El mundo que se come la comida*: `rev` depende de cuántas veces se encuentra B en Q4. Por eso el runner reporta
   `vis[B]` y `vis[A]` por cuarto **al lado de `rev`**, en los tres brazos; si las exposiciones difieren entre brazos, `rev`
   no se lee como conducta. (En este bloque los tres brazos son el mismo organismo, así que es además un chequeo del
   placebo.)
4. *Sitios fijos*: el mundo vivo tiene recursos móviles y reaparición; no aplica. Se reporta igualmente `celdas` y
   `splits` por brazo para detectar cualquier degeneración.

## 8. Mini-prueba de un proceso (humo), con números

`python experimentos/criterio_v3/corre_criterio_v3.py --humo` — un proceso, **sin Pool**, **6 corridas** de T = 100 000
(más el arnés como subproceso a T = 20 000), y **escribe su JSON** en `datos/humo/` (ERR-42):

1–4. T-A brazo VIVO, semilla 2161: OFF · PLACEBO · PEOR(m = 1.25) · PEOR(m = 1.50) → fija `m` con la regla de §6.
5–6. T-C (ii), semilla 2121: OFF · PLACEBO.

Comprueba: el arnés da 54/54; PLACEBO **difiere** de OFF (si saliera idéntico, la perilla no hace nada y el bloque se
para); el JSON se escribe; y da el único número que el humo fija (`m`).

## 9. Coste y quién lo corre

Serie: T-A 40 × 2 brazos × 3 arms = 240 corridas + T-C (ii) 40 × 3 = 120 → **360 corridas de T = 100 000**, del orden de
dE5-v2. **Lo corre el coordinador.** Yo no abro `Pool`, no commiteo y no mato procesos.

Comando de la serie:

```
JUACO_POOL=10 python experimentos/criterio_v3/corre_criterio_v3.py
JUACO_POOL=10 python experimentos/criterio_v3/corre_criterio_v3.py --replica      (2281-2320 / 2321-2360)
```

## 10. El único número que fija el humo

**`m` (multiplicador del coste de vida del brazo PEOR) = 1.50**, fijado por el humo del 21-sep 16:33–16:36
(`datos/humo/critv3_humo_20260921_163338.json`, sha `3662dcc1b522473a`; arnés
`datos/humo/identidad_v3cal_20260921_163603.json`) con la regla escrita en §6, sobre la semilla 2161, brazo VIVO:

| brazo | r | descendientes | muertes | Δr contra OFF |
|---|---|---|---|---|
| OFF (`placebo=0`) | −100 | 19 | 119 [62, 57] | — |
| PLACEBO (`placebo=1`) | −59 | 21 | 80 [46, 34] | (no aplica: es el nulo) |
| PEOR m = 1.25 | −117 | 3 | 120 [79, 41] | **−17** (no llega a −20) |
| PEOR m = 1.50 | −173 | 2 | 175 [114, 61] | **−73** (≤ −20) |

Por la regla, `m = 1.50` (el menor de los dos con Δr ≤ −20). **Declaración honesta, escrita al fijarlo:** con esa semilla
el brazo PEOR resultó **mucho más duro** que el δ = −20 pedido (−73), así que **CAL-3 se juzga con CAL-3a** (el
desplazamiento exacto de −20 sobre el reparto del nulo, que es la pregunta que importa) y el brazo PEOR queda como
control de que la letra también rechaza un empeoramiento **real** del mundo, con su Δr medido a n = 40 al lado.
`Δr` de una sola semilla tiene sd 11–19.5: el de la serie puede ser bastante distinto; se reporta, no se recalibra.
(Nota de procedencia: `umbrales_v3.PEOR['m']` ya llevaba 1.50 escrito como marcador de posición antes del humo; la regla
declarada seleccionó ese mismo valor, así que no hubo recalibración — pero queda dicho.)

**Lo que además verificó el humo:** arnés **54/54** (47 identidades + 7 controles que deben fallar); el JSON se escribe;
PLACEBO ≠ OFF en la trayectoria (r −59 contra −100 en la misma semilla: la perilla hace algo, y de paso muestra por qué
"pareado por semilla" en el mundo vivo es nominal); T-C (ii) semilla 2121: `rev` 69 (OFF) contra 35 (PLACEBO), con
`vis[B]` por cuarto 1605/1747/468/239 y 1436/1847/201/217 — las exposiciones se reportan al lado de `rev` (trampa 3).

## 11. Fallos pasados que este bloque podría repetir, y cómo se evitan

- **ERR-3 / regla 3 (recalibrar tras ver datos)** — el riesgo mayor: se cambia una letra después de que dos candidatos
  cayeran por ella. Se evita así: **nada se rejuzga**, v3 rige sólo candidatos futuros con semillas nuevas, y la
  justificación es el **nulo** (el tronco contra sí mismo), que no depende de qué candidato cayó.
- **ERR-31** (umbrales leídos de la batería): `umbrales_v3.py`, módulo único importado.
- **ERR-38 / regla 14** (entrada copiada con defaults distintos): campo a campo, en su propio script, etapa 2 del runner,
  y **para el caso raro** de que los tres brazos salieran idénticos hasta el último decimal el arnés M1/M2/M4 lo detecta.
- **ERR-39** (control de paja): el PLACEBO **no** es paja, es el nulo exacto, y CAL-4 lo verifica antes de leer nada.
- **ERR-42** (humo que no llega a escribir su JSON): el humo y el arnés escriben JSON.
- **ERR-43 / ERR-54 / ERR-87**: crudos a disco **antes** del análisis y **releídos del disco**; el JSON del subproceso se
  localiza por prefijo + sello exacto.
- **ERR-89** (una puerta que el runner no juzga): una línea impresa **por puerta y por letra**, con su umbral al lado.
- **ERR-85 / ERR-86** (CPU, Pool, matar procesos): no corro Pool; el tamaño lo fija `JUACO_POOL`; hay Pools del
  coordinador vivos y no se tocan.

Creador A-CAL, 21 sep 2026.
