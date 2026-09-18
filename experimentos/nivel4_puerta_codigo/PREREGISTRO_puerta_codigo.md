# Nivel 4 (memoria persistente) — **PUERTA DE FAMILIARIDAD POR EVIDENCIA DEL CÓDIGO EXACTO**: ¿se puede recuperar la capacidad de v11 sin volver a perder la generalización?

**Escrito ANTES de correr, 18 sep 2026.** Propuesta B-2 del creador B (`registro/investigacion/PUENTE_creacion.md`,
"Propuestas para el coordinador"). Regla 12. Ataca el canje **puerta contra capacidad**, medido y registrado el día 5.

## 0. Qué se sabe

- v13 = v11 + vía lenta + **puerta de familiaridad**: la boca consulta la vía rápida sólo si **≥ `puerta` = 3 de las 3
  celdas del código** tienen `|Wp−Wn| > 0.2`. Eso rompió el canje memoria/generalización (retención 20/20 **y** 0.85 en
  nunca vistos) y abrió otro, medido: **capacidad**. Mundo grande (10 px, 60 estímulos, semillas 41–60):
  `N*` **28** (paso 20 000) y **35** (paso 60 000) contra **43** y **50** de v11 (`reverificacion_v13_20260917_171603`).
- Diagnóstico del creador B (mundo grande reducido, D = 10, 20 estímulos, `paso_t` = 10 000, T = 200 000, semillas
  41–43): **el 100 % de los estímulos que la puerta declara desconocidos al final habían sido mordidos ≥ 5 veces**
  (3/2/5 no-familiares, de los cuales 3/2/4 con ≥ 5 mordidas). La puerta no está preguntando *"¿lo conozco?"*: está
  preguntando *"¿tengo su valor sin repartir?"*, y la fisión de v11 reparte el valor por construcción.

## 1. Hipótesis

La puerta mezcla **dos preguntas distintas**. Contando las mordidas del **código exacto** se separan:
lo **nunca visto** sigue yendo a la vía lenta (su código tiene evidencia 0 → generalización intacta) y lo **ya visto**
vuelve a la rápida aunque su valor esté repartido entre celdas → **capacidad recuperada**. Es el primer intento del
proyecto de romper un canje **desacoplando dos señales** en vez de moviendo una perilla.

## 2. Mecanismo mínimo (regla local, y qué memoria exige)

`familiar(P) ⟺ ncod[código(P)] ≥ n0`, con `ncod[código] += 1` en cada mordida. **`n0 = 5`, fijado ANTES de correr**
(orden de magnitud de mordidas por estímulo en el mundo grande; **no se barre**: si hubiera que barrerlo, se barre en
semillas distintas y se declara).

- **Memoria:** un entero por **código visto** (≤ uno por estímulo aprendido) más el orden de aparición. **Cero por
  celda.** No toca `Wp`, `Wn`, `KW` ni ninguna regla de aprendizaje: **sólo el ruteo entre las dos vías.**
- **Propiedad conocida, declarada antes de correr:** los códigos **cambian** cuando hay divisiones, así que un patrón
  cuyo código acaba de cambiar **pierde su evidencia** y vuelve a la vía lenta hasta reunir `n0` mordidas con el
  código nuevo. Es parte del mecanismo (un código recién nacido **es** nuevo), no un efecto a corregir después.
- **Homólogo biológico:** pendiente de la pregunta B-2 al explorador (lectura de familiaridad por patrón en el cuerpo
  fungiforme). Si no lo hay, se declara como muleta computacional, y la variante local por **conjunciones de pares**
  (`F[c1,c2]`, familiar si ≥ 2 de los 3 pares del código superan `n0`) queda como candidata para el paso siguiente.

## 3. Instrumentos (por anclas, sin tocar ningún original)

| archivo | origen (solo lectura) | sha origen | sha generado |
|---|---|---|---|
| `organismo_v13B.py` | `organismo/organismo_v13.py` **(CONGELADO)** | `cc8b16b492d4d324` | `59075fa17f034112` |
| `organismo_v13gB.py` | `experimentos/v13_dos_vias/organismo_v13g.py` | `2a80e125f8593bf2` | `94324c29af339673` |
| `organismo_capB.py` | `experimentos/v13_reverificacion/organismo_capD13.py` | `fd8e10435801646c` | `8070351683837077` |
| `bateria_generaliza_B.py` | `organismo/bateria_generaliza.py` | `46772f5a582872c8` | `f1da3b0a1a4ee185` |
| `organismo_v13Bn5.py` (PAT, perilla fija) | `organismo_v13B.py` | — | `d803e529f7c44a9c` |
| `organismo_v13Bn5c.py` (PATC, enmienda 1) | `organismo_v13B.py` | — | `f96db73684946a79` |
| `bateria_v13B.py` (examen v3' sobre PAT) | `organismo/bateria_v13.py` **(CONGELADA)** | `1a027bcb37eb536e` | `ef78a939fd9fd4f7` |
| `bateria_v13Bc.py` (examen v3' sobre PATC) | `organismo/bateria_v13.py` **(CONGELADA)** | `1a027bcb37eb536e` | `bed5ad9661ea7040` |

Constructor único: `construye_puerta_codigo.py`. `bateria_generaliza_B.py` es la batería con **dos entradas más** en
`INSTRUMENTOS` y las rutas corregidas por vivir fuera de `organismo/`: **los umbrales y los criterios G1/G2/K no se
tocan**, y la batería original no se modificó.

**Identidad obligatoria** (`identidad_v13B.py`): con `puerta_pat = 0, pat_shuf = 0` los tres organismos son sus
originales **bit a bit** (todas las claves) y `bateria_generaliza_B.py organismo_v13B 3` da **lo mismo, línea a línea**,
que `bateria_generaliza.py organismo_v13 3`. Si no da 21/21, el bloque no corre (S4).

## 4. Diseño

- **Bloque K (capacidad).** El montaje **exacto** de `experimentos/v13_reverificacion/`: `mundo_grande` con D = 10 px y
  **60 estímulos**, `paso_t ∈ {20 000, 60 000}` (T = 1.2 M y 3.6 M), semillas **41–60** — las mismas con las que se
  midieron 28/35 y 43/50, para comparar sin rehacer nada. Brazos:
  - **v11** `puerta=None` (referencia alta de capacidad)
  - **v13** `eta_s=0.015, puerta=3` (el tronco: referencia baja)
  - **PAT** `eta_s=0.015, puerta=3, puerta_pat=5` (la propuesta)
  - **PATSHUF** `…, puerta_pat=5, pat_shuf=1` (**control**: la puerta lee la evidencia del código **vecino** en el
    orden de aparición — mismo multiconjunto de cuentas, asignadas mal)
- **Bloque G (generalización y retención, ERR-20).** `bateria_generaliza_B.py organismo_v13B_n5 20 --desde 101 --log`
  (las semillas del examen de congelación de v13) y `bateria_v13.py` sobre `organismo_v13B` con `puerta_pat=5`.
  **Sin este bloque el resultado de capacidad no significa nada**: recuperar capacidad pagando generalización sería el
  mismo canje con otro nombre.
- Comparaciones **pareadas semilla a semilla**; medianas y rangos (regla 6).

## 5. Predicciones numéricas (las de la propuesta B-2, sin tocar)

- **Q1 (capacidad).** `N*(PAT)` ≥ **45** con `paso_t = 20 000` y ≥ **48** con 60 000 (v13: 28 y 35; v11: 43 y 50),
  y **`N*(PAT) > N*(v13)` en ≥ 15/20 pareado** en los dos pasos.
- **Q2 (no toca el aprendizaje).** `celdas` y `divisiones` de PAT dentro de **±2** de las de v13 (mediana), porque el
  mecanismo sólo cambia el ruteo.
- **Q3 (la puerta deja de equivocarse).** `nofam_fin(PAT)` **≤ 2** de 60 (v13: la mediana registrada de no-familiares
  al final), y de los estímulos que PAT manda a la lenta, **ninguno** con evidencia ≥ `n0`.
- **Q4 (generalización intacta).** En `bateria_generaliza_B` con `organismo_v13B_n5`: **G1 ≥ 0.80 y G2 ≥ 0.85**
  (los valores de v13 en 101–120) y **K** con cobertura; y `bateria_v13.py` **8/8** (criterio v3').

## 6. Controles que pueden fallar, y sus cláusulas (escritas antes)

- **S1 — el control que de verdad puede matarla: la GENERALIZACIÓN.** Si al abrir la puerta por evidencia el organismo
  empieza a leer con la vía rápida patrones **nunca vistos** (por colisión del código exacto entre un patrón nuevo y
  uno aprendido), **G1/G2 caen hacia el 0.60 de v11** y la propuesta queda **REFUTADA**: sería recuperar capacidad
  pagando otra vez la generalización. Umbral: G1 < 0.70 o G2 < 0.75 ⇒ refutada, y se registra como "el canje se
  desplaza, no se rompe" (la misma frase que ya se ganó la novedad de sitio).
- **S2 — contadores barajados (PATSHUF).** Si PATSHUF iguala a PAT en `N*` (diferencia de medianas ≤ 2 y PAT > PATSHUF
  en < 14/20 pareado), lo que actúa es **"abrir la puerta"**, no la evidencia del código: entonces la propuesta se
  degrada a "la puerta de v13 es demasiado estricta" y lo que hay que preregistrar es bajar `puerta` de 3 a 2, no
  contar códigos. Es más barato y habría que decirlo así.
- **S3 — retención.** Si `bateria_v13.py` no da 8/8 con la perilla encendida, la puerta por código rompe algo del
  examen del tronco y el bloque se cierra sin tocar v13.
- **S4 — inercia.** Si la etapa de identidad no da 21/21, no se corre nada (un instrumento que no es bit a bit con la
  perilla apagada no confirma nada).
- **Vocabulario permitido según el resultado.** Si pasan Q1–Q4: *"contar las veces que ha mordido cada código le
  devuelve la capacidad sin costarle la generalización"*. Si cae S1: *"el canje puerta/capacidad se desplaza, no se
  rompe"*. Si cae S2: *"la puerta de v13 es demasiado estricta; contar códigos no aporta sobre bajarle el umbral"*.
  En ningún caso "reconoce", "recuerda haber visto" ni "sabe lo que conoce".

## 7. Mini-prueba que originó la propuesta (3 semillas, escala REDUCIDA, humo, NO confirmatorio)

D = 10, **20** estímulos, `paso_t` = 10 000, T = 200 000, semillas 41–43. **No mide generalización.**

| brazo | `N*` (41/42/43) | mediana | `M_max` | a la lenta | de ellos mordidos ≥ 5 | celdas |
|---|---|---|---|---|---|---|
| v13 (puerta por celdas = 3) | 6 / 5 / 6 | **6** | 13 | 3 / 2 / 5 | **3 / 2 / 4 (todos)** | 71/69/65 |
| v11 (sin puerta) | 9 / 20 / 20 | **20** | 15 | 0 | 0 | 71/67/65 |
| **PAT (puerta por código, n0 = 5)** | 12 / 20 / 20 | **20** | 14 | 0 / 1 / 1 | — | 71/67/65 |

El canje se reproduce a esa escala (v11 > v13 en 3/3) y la puerta por código lo cierra (≥ v13 en 3/3, mediana igual a
v11) **con las mismas celdas**. Lo que esa mini-prueba **no** puede decir es lo único que decide el bloque: si la
generalización sobrevive (S1).

## ENMIENDA 1 (18 sep 2026, escrita ANTES de la serie y DESPUÉS del humo de 2 semillas; se declara así)

**Qué vi en el humo, y no lo escondo.** Al probar el montaje con `bateria_v13B.py 2` (la batería del tronco apuntando
a v13 + puerta por código, `n0 = 5`), el criterio **3''** del examen v3' **FALLA 0/2**: "la vía lenta activa sin
plasticidad con A∩B = 3 separa por píxeles" deja de cumplirse. **Diagnóstico mecánico:** con A∩B = 3 los canales `Wp`
y `Wn` de las celdas compartidas se saturan juntos (BUG-01) y `|Wp−Wn| ≤ 0.2`, así que **la puerta de v13 no es sólo
un detector de familiaridad: es también un detector de CONFLICTO**, y manda a la vía lenta justo los códigos cuyo
valor está anulado. Contar mordidas del código **pierde esa función**: un patrón conflictivo tiene muchas mordidas y
vuelve a la rápida, donde `W ≈ 0`.

**Enmienda (no es recalibrar un umbral: es un mecanismo distinto, con su propia predicción y su propio brazo).**
Se añade el brazo **PATC**: `familiar(P) ⟺ ncod[código(P)] ≥ n0` **Y** `≥ pat_min` celdas del código con
`|Wp−Wn| > 0.2`, con **`pat_min = 1`**. Es exactamente la rama que `CLAUDE.md` deja abierta desde el día 5 —
*"una puerta que consulte la lenta sólo con la rápida vacía, para recuperar capacidad sin perder generalización"*—
más la evidencia del código. `n0 = 5` y `pat_min = 1` quedan fijados aquí y **no se barren**.

- **Predicción de la enmienda:** PATC cumple Q1–Q4 **y además** pasa el examen v3' completo (3' y 3''), que es lo que
  PAT no pasa. Humo de 2 semillas con `bateria_v13Bc.py 2`: **los ocho criterios PASAN** (incluido 3'' 2/2), frente a
  `bateria_v13B.py 2` donde 3'' da 0/2. Dos semillas no deciden nada: lo decide la serie en 101–120.
- **Cláusula:** si **PAT** no pasa el examen v3' en 20 semillas (que es lo que el humo anuncia) pero **PATC** sí y
  además cumple Q1, **lo que se declara es PATC**, y PAT queda registrado como *"contar el código sin exigir valor
  pierde el detector de conflicto de la puerta de v13"* — un hallazgo sobre lo que la puerta de v13 estaba haciendo
  además de lo que creíamos. Si **ninguno de los dos** pasa S1 (generalización) o el examen v3', el bloque se cierra
  **sin tocar v13** y el canje puerta/capacidad queda como está.
- **Brazos definitivos del bloque K:** `v11 · v13 · PAT · PATC · PATSHUF` (5 × 2 pasos × 20 semillas = 200 corridas).


## Enmienda 2 (coordinador, 18 sep 2026, 02:45; escrita DESPUÉS de la serie 41–60 y ANTES de la réplica del examen)

Resultado de 41–60: Q1 OK a 60 000 (PATC 50.5 ≥ 48, > v13 19/20), NO a 20 000 (41.5 < 45), Q2/Q3/S2 OK, S1 generalización OK
(px0 1.000 / G2 0.96), retención: PATC pasa 3', 3'', celdas, 4a–4d y cinco etapas 20/20, **E2 19/20** (`come B Q4 ≥ 50`), PAT
falla 3'' (como predijo la enmienda 1). **Réplica del examen v3' de PATC en semillas nuevas 121–140** (`bateria_v13Bc.py 20
--desde 121 --log`), **misma letra** (8/8 exigidos; ningún umbral cambia). Si pasa, PATC entra a `PROPUESTA_v14.md` como
tercer candidato; si E2 (u otra etapa) vuelve a caer, la puerta por código queda como órgano de experimento y la lectura
registrada es: *recupera la capacidad y conserva la generalización, pero reabrir la vía rápida antes de tiempo cuesta una
semilla de conducta en el examen*. El criterio Q1 a 20 000 no se retoca: se registra como no alcanzado.
