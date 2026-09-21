# JUNTA 21-sep-2026 — PROPUESTA DEL CREADOR C (sistemas vivos y mente)

Misión: llegar a la AGI por este camino. Todo lo de abajo es **lectura de solo-lectura + una mini-prueba propia de un
proceso**; nada se rejuzga, nada se commitea, ningún congelado se tocó. Instrumento propio por anclas en esta carpeta.

## 1. Avance por nivel del brief (porcentaje = lo declarado CON réplica)

| n | % | una frase, con la entrada |
|---|---|---|
| 1 asociar | **100** | cerrado día 2–4; batería del tronco lo protege (`bateria_v142`). |
| 2 desaprender | **100** | cerrado día 4 con v9 (memoria de rechazo); reversión conductual E2 en el examen. |
| 3 generalizar | **100** | v13→v14.1: G1 1.000 / G2 0.967 en 101–120 (ESTADO, "Tronco"). |
| 4 capacidad / no confundir | **95** | cerrado; el negativo que faltaba (alias de código) lo repara B-5 = **v14.2**, 18/18 (HANDOFF 21:25). Falta el techo real de capacidad: el mundo de 60 se queda corto. |
| 5 comunicación | **75** | N1 cerrado; referencia de **familia exacta O variante**, no las dos con la misma tabla; BA-v cae **P6 en 961–980 (13/19) y en 981–1000 (14/18)** (HANDOFF 15.17 + log `serie_bav_s981-1000`). |
| 6 mapa / dos metas | **50** | rodeo replicado; *elige y rodea, no planifica*; el canje del mapa es estructural y v14 no lo lleva (CLAUDE.md día 7). |
| 7 composición / XOR | **85** | 3T-k compone hasta 3; XOR cerrada como **prior de pares declarado**; **LÍNEA CERRADA** v15c–v15g: ninguno entra (HANDOFF 15.16). |
| 8 aprendizaje abierto | **40** | curiosidad por progreso refutada; el mundo vivo de dos necesidades es el primer mundo con más de una dimensión de valor. |
| 9 autonomía / modelo de sí | **30** | C-P1 y dE replicados ×2–3; **fase 9 bloque 1: 8/10 puertas, SIN réplica** → no sube de 30 hasta 1521–1540 (HANDOFF 15.18). **H-1/ERR-62 siguen en pie: ningún brazo cruza R₀ ≥ 0.90.** |
| 10 alma / familias / vivo | **10** | exploratorio: el alma razonada no gana al azar; el nodo **sí** transmite contenido. |

---

## 2. Q3 (a) — La letra de F9-4 **NO** mide lo que quería medir. La que sí: **F9-4bis (ERR-91)**

**El fallo es de diseño, no de dato.** F9-4 pedía `p1(REL_BAR) ≤ p1(NADA)+0.15`. Pero `p1` es una **tasa de un solo
lado** (rechazar lo malo), y el propio preregistro escribió en §6 que *"`p1` sube gratis si el cuerpo muerde menos"* —
y luego **aplicó esa cautela sólo al candidato** (puerta doble en F9-3, brazo REL_FIJO) y **no al control**. Un nodo
barajado destruye la asociación patrón↔recompensa pero **conserva las marginales**: el lector recibe muchas R = −3 sin
patrón correcto, baja su valor de todo y se vuelve genéricamente cauto. Eso sube `p1` sin un bit de contenido. La
huella está en el mismo veredicto: `c1(REL_BAR) = 0.598` contra 0.99 en todos los demás brazos.

**La letra que sí lo mide — índice de DISCRIMINACIÓN del cuerpo nuevo (Youden), por corrida:**

```
J = p1 + c1 - 1        (por CORRIDA, no mediana de medianas)
```

`J = 0` para las **dos** políticas degeneradas (morder todo: p1=0,c1=1; no morder nada: p1=1,c1=0). **Por construcción
no se puede subir con cautela genérica**: es la trampa 2 cerrada en la métrica, no en un brazo aparte.

**F9-4bis (semillas NUEVAS 1541–1560, réplica 1561–1580; no rejuzga 1501–1520):**
1. `A₁₂(J: REL > REL_BAR) ≥ 0.85` **y** `J(REL_BAR) ≤ J(NADA) + 0.10` (el nodo barajado **no compra discriminación**).
2. Se conserva la mitad que ya estaba: `A₁₂(vida REL > REL_BAR) ≥ 0.80`.
3. **Brazo nuevo que puede tumbarla: `CAUTELA`** = `nodo=0` + un empujón **negativo constante** en la boca
   (`sesgo_fijo = −c`, el mismo mecanismo del brazo `CONST` de C-P1), con `c` **fijado en el humo** para igualar
   `c1(REL_BAR)`. Si `CAUTELA` reproduce la vida y el `J` de REL_BAR, entonces *"el nodo barajado = cautela genérica"*
   queda **medido**, no inferido. Si `CAUTELA` **no** lo reproduce, lo que REL_BAR aporta no es cautela y **mi
   diagnóstico queda refutado**.
- **Refuta F9-4bis:** `J(REL_BAR) > J(NADA)+0.10`, o `A₁₂ < 0.85` → lo heredable **sí** sería la magnitud y no el
  contenido. **Predicción: J(REL) 0.90–0.98 · J(REL_BAR) 0.05–0.25 · J(NADA) 0.10–0.25 · A₁₂ 0.95–1.00.**
- **Declarado:** las medianas publicadas de 1501–1520 *sugieren* esto, pero **no son el veredicto** (J de medianas ≠
  mediana de J, y la letra se escribió después de ver la serie: por eso va con ERR y semillas nuevas, regla 3).

---

## 3. Q3 (b) — El bloque 2: **mi hipótesis favorita está REFUTADA por mi propio humo**, y eso da el bloque

**Diagnóstico (solo lectura del crudo, no es puerta).** Con `acum=1`, `R₀ ≈ vida_media × sac_frac / rep_X`: REL da
597 × 0.49 / 500 = 0.59 (medido 0.494). **Para R₀ ≥ 0.90 hace falta `vida × sac ≥ ~536`; hoy es 293: falta 1.8×.** Las
muertes de REL son **todas por necesidad** (hambre 66 + sed 87 ≈ 154 cuerpos): el recién nacido ya no se envenena
(`p1` 0.96), se queda sin agua y sin comida. El techo del brazo inmortal RENACE es R₀ 1.08, así que REL está al 46 %
del máximo del mundo.

**Mi hipótesis C-F9B (escrita antes de correr):** el nodo transmite la **regla** (vía lenta, lineal) y no los **casos**
(vía rápida, Kenyon). Perilla `nodo_via=1`: el mensaje entra **también** por la vía rápida con la **misma regla local
de la mordida** y cuenta como evidencia del código (`ncod`), porque si no la puerta de v14 jamás la consulta.
**Memoria nueva: CERO.**

**Humo (6 corridas, un proceso, T = 100 000, semillas 1–2 YA VISTAS; `datos/humo/f9b_humo_20260921_160425.json`):**

| brazo | s | acum | R₀ | vida | p1 | c1 | **J** | sac | expA | via_msg | fam_nac |
|---|---|---|---|---|---|---|---|---|---|---|---|
| REL | 1 | 1 | 0.423 | **549.5** | 0.960 | 1.000 | **0.960** | 0.483 | 561 | — | — |
| **REL2** | 1 | 1 | 0.415 | **209.0** | 0.752 | 0.986 | **0.738** | 0.554 | 745 | 11265 | 2.62 |
| REL | 2 | 1 | 0.484 | **601.0** | 0.960 | 0.974 | **0.934** | 0.483 | 614 | — | — |
| **REL2** | 2 | 1 | 0.450 | **208.0** | 0.771 | 1.000 | **0.771** | 0.579 | 764 | 10426 | 2.44 |
| REL | 1 | 0 | **0.4076** | **598.0** | 0.9603 | 1.000 | 0.960 | 0.523 | 631 | — | — |
| REL2 | 1 | 0 | 0.305 | 201.5 | 0.731 | 0.992 | 0.723 | 0.590 | 637 | 10315 | 2.55 |

**HB1 0/2 · HB2 0/2 · HB3 0/2 · HB4 3/3 · HB5 6/6 · HB6: el ancla es exacta** (REL acum=0 s=1 reproduce dígito a
dígito el humo del bloque 1: R₀ 0.4076→0.408, vida 598, p1 0.9603, c1 1.000; el 0/1 es sólo mi tolerancia de 1e−9).
**Mis tres predicciones de hipótesis quedan refutadas por mi propio humo: leer con las dos vías ACORTA la vida a 0.38×
y hunde la discriminación de 0.96 a 0.74.**

**Por qué, y es el hallazgo:** la puerta de v14 **sustituye, no suma**. La vía lenta lee a `eta_s = 0.15` y satura el
veneno cerca de −3 en pocos mensajes; la rápida lee a `eta = 0.03` sobre 3 celdas y tras 50 mensajes va por ≈ −1. En
cuanto la lectura da evidencia (`ncod ≥ 5`), la boca **abandona el −3 bueno y usa el −1 malo**: come más (sac 0.48 →
0.57, expA 561 → 745) y se muere el triple de rápido. Comprobado en el mismo estado final (T = 20 000, las mismas
llamadas del arnés): con `nodo_via=1`, `W(B)` de la rápida = **−2.26** contra `W_lenta(B)` = **−2.64**, y `W(D)` cae de
−2.10 a −0.61.

### El bloque 2 que propongo (un cambio, con el modo de fallo YA medido)

**Hipótesis C-F9B′.** *Leer llena la memoria; morder abre la puerta.* Perilla `nodo_via=2`: el mensaje entra por la vía
rápida **sin tocar `ncod`**. La puerta sigue abriéndose sólo con las mordidas **propias** del cuerpo; cuando se abre,
la vía rápida **ya trae los casos del linaje**. Memoria nueva: **CERO** (es `nodo_via=1` menos una línea).
- **Instrumento y anclas:** `construye_f9b.py` (ya escrito, 6 anclas) desde `organismo_f9.py` `3a821884394d66c9` ←
  `organismo_alma2` `4fd616aeaf535e61` ← … ← **TRONCO CONGELADO `organismo_v14.py` `feefc88b1fd8d434`**. Arnés
  `identidad_f9b.py`: **66/66** (salida pegada en `identidad_f9b_salida.txt`).
- **Brazos:** NADA · REL (`via=0`) · **REL2b (`via=2`, el candidato)** · REL2 (`via=1`, **el fallo medido, se corre para
  que quede en el registro**) · REL2b_BAR (contenido) · REL_BAR · CAUTELA (§2). Dos niveles de `rep_acum`.
- **Predicción numérica (1581–1600, réplica 1601–1620):** vida(REL2b) **[600, 1000]** (1.0–1.7× REL) · `J`(REL2b)
  **≥ J(REL) − 0.03** · `R₀`(REL2b, acum=1) **[0.50, 0.80]** · **probabilidad de cruzar 0.90 que declaro: 15 %**, y lo
  digo antes: **si no cruza, H-1 y ERR-62 siguen en pie** y lo que falta no es más conocimiento sino **dónde** (el
  mapa, nivel 6) o un mundo con más de un cuerpo a la vez. La aritmética de arriba no deja otra salida honesta.
- **Control que puede fallar:** **DOSIS** — REL con `eta_s` al doble (mismo delta total, una sola vía). Si DOSIS iguala
  a REL2b, lo que paga es **cantidad de aprendizaje**, no **dos vías**, y el mecanismo se renombra.
- **Qué lo refuta:** vida(REL2b) < 1.1× REL, o `J`(REL2b) < `J`(REL) − 0.03 (volvió la sustitución), o REL2b ≡ REL en
  todas las claves (perilla inerte: ERR-38).
- **Semillas NUEVAS: 1581–1600 y 1601–1620** (verificadas libres: `grep` en `*.py`/`*.md` sin apariciones y barrido de
  los 562 JSON de `datos/` con máximo 2080). **Ojo: 2101–2120 ya NO están libres** — el coordinador lanzó ahí la
  tercera serie de BA-v a las 16:06.

---

## 4. Q3 (c) — dE5 sin morder más veneno: **dE5-fam**, y por qué NO propongo bajar la dosis

Lo medido: recuperación 1 269 contra 4 095 (**3.23×**), `CONST` sin información 5 247 (**el control funciona**), se
apaga sola (`sesgo_q` Q1 0.076 / Q2 0.0001 / Q3 0.0996 / Q4 0.0001) y **el único número que la tumba es
`mord_post` 61.5 contra 54.5 = 1.128 > 1.10** — siete bocados en 100 000 pasos.
- **"Dosis menor" la descarto**: es recalibrar una perilla para que pase un criterio después de verlo (regla 3), y el
  canje ya está medido en `PREREGISTRO_dosis_dE.md` (k=3 cae el examen).
- **"Sólo tras el cambio" ya ocurre**: Q2 y Q4 son 0.0001. No hay nada que arreglar ahí.
- **"Sólo para lo familiar" NO funcionaría y lo digo antes de que nadie lo corra**: tras la inversión el veneno nuevo
  es **A**, que es el patrón MÁS familiar (W = +1 consolidado) → la puerta estaría abierta justo donde sobra.

**Lo que propongo: `dE5-fam` = la sorpresa empuja sólo donde el valor dice NO.**
`Vb += k_sorp·_sbE · [w < 0]` (el valor de la boca ya está calculado en esa misma línea: `_wt`). **Memoria nueva: CERO,
constantes nuevas: CERO.** Argumento *a priori*, no de dato: con `w > 0` y hambre la boca ya muerde
(`pb ≈ 1`), así que el empujón ahí es **funcionalmente redundante y sólo suma veneno**; con `w < 0` es donde el
empujón hace su trabajo (volver a probar lo que rechazo). Post-cambio: **B** (ahora comida, w = −3) recibe el empujón →
la recuperación se conserva; **A** (ahora veneno, w = +1) **no** lo recibe hasta que su propio valor baja, y para
entonces `_sbE` ya decayó.
- **Preregistro:** las **siete puertas del CRITERIO v2 completas**, semillas **NUEVAS 2201–2280** (2001–2080 usadas por
  dE5, 2101–2120 por BA-v), instrumento por anclas desde `organismo_v15_dE5.py` con **una** inserción, arnés con el
  control `M8: dE5-fam ≠ dE5` y la identidad `k_sorp=0 ⇒ v14.2 bit a bit`.
- **Predicción:** `mord_post` **0.98–1.08 ×** OFF (pasa G-5) · recuperación **0.30–0.50 ×** (2–3.3×, es decir
  **peor que dE5 y lo firmo**) · T-E E1 veneno total **1.00–1.06 ×**. **T-A y T-C(ii) las sigo viendo en 0.40–0.60**:
  por la letra de hoy **cae igual** (ver Q1). **Probabilidad de cruzar las siete: 15 %; de cruzar T-E y T-G: 55 %.**
- **Control que puede fallar:** `dE5-neg` con el empujón **sólo donde w > 0** (el complemento). Si `dE5-neg` recupera
  igual que dE5-fam, la asimetría no es el mecanismo y mi argumento se cae entero.
- **Qué lo refuta:** recuperación > 0.60× OFF (la puerta G-1 muere) o `mord_post` > 1.10× igual.

---

## 5. Q1 — Voto: **T-A y T-C(ii) son puertas de NO-REGRESIÓN con el umbral puesto sobre la hipótesis nula**

`T-A` exige `A₁₂ ≥ 0.50` pareado. Para un candidato **exactamente igual** al tronco, A₁₂ = 0.50 y el error estándar
con n = 20 es ≈ 0.13: **un candidato neutro cruza esa puerta con probabilidad ≈ ½ — es una moneda, no un criterio.**
v15f dio 0.4–0.55 y dE5 0.40/0.50: es la banda del nulo, exactamente lo que el coordinador vio como "observación
transversal". `T-C(ii)` es distinta: su umbral es **0.75**, o sea una **exigencia de capacidad** escondida dentro de
una puerta que se llama "se desdice" (la forma de no-regresión ya la lleva T-C (i), conducta E2 ≥ 18/20).
**Voto:** (1) T-A pasa a **no-inferioridad**: medianas como están **y `A₁₂ ≥ 0.35`** (margen, no nulo). (2) T-C(ii) se
**mueve a T-G**: si un candidato declara "revierte mejor en el mundo vivo" como su capacidad, que lo declare y lo mida
ahí con su control barajado; T-C se queda con (i). (3) La capacidad vive **sólo** en T-G — cobrarla dos veces es lo
que produjo tres candidatos rechazados por ruido. **Entra como ERR-92, con fecha, y NO rejuzga a nadie** (regla 3:
v15c–v15g, B-5 y dE5 quedan como están; el primer candidato que lo use son semillas nuevas).
**Predicción:** con la letra nueva, el próximo candidato con capacidad real dará T-A A₁₂ en **[0.40, 0.60]** y pasará,
y **ninguno** de los ya medidos habría cambiado de veredicto por esto solo (v15f cae también por T-D y T-E; dE5 por
T-E y T-G): la corrección **no regala** ningún tronco, sólo deja de sortearlo.

## 6. Q2 — Voto: **cerrar la fase 5 en 75 %** (con una sola reapertura posible)

BA-v cae P6 en **dos** series nuevas (13/19 y 14/18) y su propio preregistro §172 escribió que eso lo cierra. Lo
declarable ya está medido y es un resultado: *"con esta tabla la referencia es de familia exacta O de variante, no las
dos"*. **La única reapertura que vale un preregistro — y es del brief, no de la letra — es `V-5`: la variante deja de
ser una etiqueta que compite y pasa a ser una CONSECUENCIA que contradice.** Mecanismo: **B-5 trasplantado a la tabla
de referencia** — cuando la entrada de una familia recibe una consecuencia cuyo signo o magnitud contradice su valor
bajo una retina distinta, **se parte** en una entrada de variante; no se escribe sufijo ninguno mientras la variante
se comporte como su familia. Memoria nueva: cero estructuras (reusa la fisión ya declarada). **Predicción: BAR-T 2–5 y
dist(PAR) 13–17; probabilidad de cruzar la misión cruda ×2: 25 %.** Si el director prefiere no gastar el Pool, mi voto
es **cerrar** y llevarse el hallazgo negativo, que es honesto y publicable.

## 7. Fallos pasados que mi idea podría repetir, y cómo los evito

**ERR-38** (perilla inerte / batería copiada sin campos): el arnés exige `nodo_via=1 ≠ 0` en 5 brazos y la medida
`fam_nac` prueba que **la puerta se abre** (no basta con que cambien los pesos). **ERR-60** (colisión de rng): ninguna
línea insertada consume el rng del mundo — el constructor lo verifica con regex y el arnés con los casos (G) y (H).
**ERR-37/61** (pareado donde no toca): R₀, vidas y `J` son integrales de trayectoria → **A₁₂ sin parear**. **ERR-87**
(`startswith` en `lee_json`): mis salidas llevan prefijo + sello exacto. **ERR-89** (una puerta que el runner no
juzga): las puertas se imprimen **una por línea** en el log. **ERR-31** (umbrales de la batería en vez del
preregistro): los umbrales de §2–§4 están **en este archivo**, antes de las series. **ERR-46..49** (la medida del
colateral): por eso `J` y no `p1`.

**Las cuatro trampas.** (1) *Canal simétrico*: n/a, el que muere escribe y el que nace lee; nadie se lee a sí mismo.
(2) *Acierto sin balancear*: **es la trampa de esta propuesta** y por eso la métrica pasa a ser `J`, que vale 0 en las
dos políticas degeneradas, más el brazo `CAUTELA`. (3) *El mundo que se come la comida*: `exp_A` se reporta por brazo y
**REL2 encuentra MÁS comida que REL** (745 vs 561), así que la medida se le pone más difícil, no más fácil.
(4) *Sitios fijos*: `spawn()` sortea y el recién nacido aparece en `rng.integers(L)`.

## 8. Mis predicciones refutadas hoy, y lo que no pude verificar

1. **REFUTADA por mi propio humo:** *"leer el nodo con las dos vías alarga la vida y sube R₀"*. Lo contrario: vida
   0.38×, `J` 0.96 → 0.74. HB1 0/2, HB2 0/2, HB3 0/2.
2. **REFUTADA antes de correr nada:** mi primera idea para (c) era *"la sorpresa sólo para lo familiar"*; la descarté
   yo mismo al ver que tras la inversión el veneno nuevo es el patrón **más** familiar.
3. **No verificado:** `nodo_via=2` (el candidato real del bloque 2) **no se corrió** — agoté las 6 corridas del
   presupuesto en el humo que me refutó. Tampoco corrí `dE5-fam`, ni `CAUTELA`, ni `V-5`: van como preregistros.
4. **No verificado:** que `vida_med` de REL_FIJO salga exactamente 600.0 en los dos niveles de `rep_acum` me huele a
   cuantización por `rep2_regalo=600`; **no lo investigué** y lo dejo anotado como posible cabo del instrumento.

**Archivos:** `construye_f9b.py` · `organismo_f9b.py` (`6a57e9fa9514099b`) · `identidad_f9b.py` +
`identidad_f9b_salida.txt` (**66/66**) · `corre_f9b.py --humo` · `datos/humo/f9b_humo_20260921_160425.{log,json}`.
