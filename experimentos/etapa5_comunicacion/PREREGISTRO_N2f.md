# Etapa 5, N2f — reaparición **con rotación** y un receptor que no se deja desenseñar

**Versión 2, escrita ANTES de correr, por decisión del coordinador del 17 sep 2026 (día 6).** Bloque 5 del plan
(`registro/PLAN.md`). Rol: diseñador de preregistros (`registro/EQUIPO.md`). Base: tronco **v13**.
Instrumento: `mundo_social_n3.py` regenerado por `construye_n3.py`; runner `corre_N2f.py`.

**La versión 1 de este preregistro (N2b tal cual en el mundo `regen=50`) NO se corre.** Su humo la mató antes de gastar
el `Pool`, y las dos perillas de esta versión salen de ese humo. Queda registrada abajo (§1) porque es la evidencia que
justifica cada cambio.

## 1. Qué dijo el humo de la versión 1 (semilla 81, un proceso; `datos/N2f_humo_s81_20260917_214216.json`, `0a8171eb466e2f89`)

| medida | N2d (mundo viejo) | **N2f v1 (`regen=50`)** | lectura |
|---|---|---|---|
| emisiones del experto rechaza / muerde | 36.365 / 564 (**0.016**) | **19.335 / 5.524 (0.286)** | `regen` reequilibra ×18 el muestreo… |
| visitas comida / veneno (experto) | 210 / 9.617 (1 : 46) | **5.499 / 19.360 (1 : 3.5)** | …pero **por objeto sigue ~7 : 1** (el veneno rechazado no se retira nunca) |
| contraste `C[s]` del receptor | ±0.34 | **−1.28 / +1.28** | **por primera vez en la línea hay magnitud** (M = [+1.00, −1.565]; 6.272 decodificaciones contra 0 en N2b) |
| veneno del novato CONV / N0 | 249 / 316 | **135 / 34** | **el símbolo HACE DAÑO**, 4× peor |
| patrones presentes | 20 | **5** (3 comidas, 2 venenos) | el mundo **se congela**: `spawn()` no vuelve a sortear y los 10 de test nunca aparecen |
| veneno Q4 del novato (N0) | — | **3** | el novato ya lo sabe todo en Q2: **K3 caería por construcción** |

Dos causas, medidas en los valores y no supuestas:

1. **El mundo se congela.** `retirar` mete el objeto en `pend` y `spawn()` sólo rellena hasta `len(objs)+len(pend)`:
   los 8 objetos del sorteo inicial (sólo de `tren`) se repiten 200.000 pasos. Es el fallo S4 de N3c otra vez
   (*el receptor ya sabe*): sin patrones nuevos no hay nada que un símbolo pueda comprar.
2. **El símbolo, ya con magnitud, desenseña.** El novato de N0 aprende los venenos a `W = −2.45 / −2.34`; el de CONV se
   queda en **−1.29 / −1.36**, que es exactamente el valor del símbolo. Con `|C| = 1.28 ≥ u_m = 1.0` la puerta vicaria
   abre 6.272 veces y arrastra el valor del patrón hacia `R̂ = ±1.28`, un **promedio de dos niveles** (uno para todas
   las comidas, otro para todos los venenos) **más grosero que lo que el receptor ya sabía** (−3). El experto no miente:
   no muerde `010110` ni una vez en 9.700 visitas. **El símbolo enseña al que no sabe y desenseña al que sabe.**

## 2. Las dos perillas (separables, en brazos distintos, las dos apagadas por defecto)

Construidas **por anclas** en `construye_n3.py` sobre el texto ya parcheado de N3/N3c/N3d; `mundo_social_n3.py`
regenerado. Ninguna edición a mano.

1. **MUNDO — `regen_rota=True`** (`Mundo._reaparece`): al reaparecer un sitio, el tipo **se vuelve a sortear** de
   `self.tipos` con el RNG del mundo, en vez de volver el mismo. Así hay **reaparición en el mismo sitio** (visitas
   equilibradas, lo verificado en N3c/N3d) **y flujo de patrones** (los 10 de test aparecen; `tipos` ya tiene los 20
   desde `t = 0`). Se aplica en los dos sitios donde un objeto vuelve al mundo: `regenerar()` y la rama de emergencia
   "nunca vacío" de `retirar()`. Con `regen_rota=False` devuelve el mismo tipo y **no toca el RNG**.
2. **RECEPTOR — `escucha_si_no_sabe=True`** (`Organismo.recibir_simbolo`): el empujón vicario del símbolo **sólo se
   aplica si `abs(self.valor(kk)) < abs(R_hat)`**. El que ya sabe del patrón más de lo que el símbolo dice no se deja
   desenseñar; se cuenta en `no_desensena`. Es la consecuencia directa de §1.2. Con la perilla apagada `valor(kk)` ni
   se evalúa (cortocircuito) y `valor`/`kenyon`/`code` no tocan estado ni RNG: **idéntico a lo actual**.
   Nota declarada: la perilla viaja en `kw_org`, así que vale para **los dos** organismos (el canal de N2 es simétrico:
   los dos emiten y los dos oyen). No es un privilegio del novato.
3. **MUNDO — `vida = int`** (`Mundo.caducar`, tercera perilla, añadida tras el humo de la v2; ver ENMIENDA 1):
   cada objeto lleva un **sello de nacimiento** y caduca en `t_nace + vida`; al caducar **se retira por el mismo camino
   que una mordida** (`retirar` → `pend`/`regen` y rotación según las otras perillas). Sin ella el veneno rechazado
   nunca sale del mundo y el mundo se absorbe en veneno. Con `vida=None` no se llama a `caducar` y el sello es
   contabilidad que no toca el RNG: **idéntico a lo actual**. Se cuenta en `caducados`.
   **`vida = 100`, valor FIJADO POR EL HUMO** (ENMIENDA 2), por las puertas de validez y **no** por el resultado.

**Identidad de las tres perillas (ya corrida, `identidad_n2f.py`, T = 60.000, semillas 81–82): 8/8 IDÉNTICO** contra el
módulo anterior a N2f (`e6b3ee1ef5b8a4be` → `ef227f833c5bf46a`) en las cuatro rutas que importan: tronco con
`regen=None`, vía de símbolos con `regen=None`, vía de símbolos **con `regen=50`**, y el montaje de N3c/N3d (conducta +
máscaras + `regen=50`). **N3c/N3d quedan protegidos.**

## 3. Hipótesis

Con **reaparición en sitio y rotación de tipos** (visitas equilibradas *y* patrones nuevos toda la corrida) el símbolo
adquiere **magnitud**; y con el receptor que **no se deja desenseñar**, esa magnitud por fin **paga**: el novato usa el
símbolo donde no sabe y conserva lo que ya aprendió mejor que el símbolo.

## 4. Diseño

Mundo de los seis brazos: `mundo='regla'`, `regla='azar'`, **`regen=50`, `regen_rota=True`, `vida=100`**, `T = 200.000`,
`nobj_por_org = 4`. Perillas de N2b en todos los brazos con símbolos: `gamma_sim = 1.2`, `baseline_q = True`,
`u_m = 1.0`, `rho_b = 0.05`, `estado_emisor = 'conducta'`, `alinea = False`, `K_sim = 2`, `beta_q = 2`, `eta_q = 0.1`,
`eta_m = 0.1`, `tau_s = 200`, `tau_m = 200`, `d_senal = 5`, `f_vicaria = 1/3`. **Semillas 81–100** (nuevas para la
línea N2: N2–N2e usaron 1–20).

| brazo | organismos | señal | `escucha_si_no_sabe` | para qué está |
|---|---|---|---|---|
| SOLO | novato | — | — | línea base sin nadie; **mide K3** |
| N0 | novato + experto | ninguna | — | la presencia sin señal (denominador de E4) |
| INNATO (= N1) | novato + experto | conducta (significado dado) | — | referencia de "significado regalado" |
| **CONV** | novato + experto | **símbolos aprendidos** | **True** | **el brazo que decide E1–E5** |
| **CONV_MUNDO** | novato + experto | símbolos aprendidos | **False** (escucha como N2b) | **atribución**: separa el mundo de la puerta |
| SHUF | novato + experto | símbolos **barajados** | True | control del punto 14 |

**Progenitor del experto: como en N2b** — `run(seed, n=1, mundo='regla', regla='azar', T = 200.000, regen=None,
devolver_estado=True)`, sin `regen` y sin rotación. Razón declarada: con `n = 1` el mundo usa el RNG del **propio
organismo** (`compat=True`), así que un progenitor con `regen` viviría en un mundo distinto del de la corrida
(`seed + 900000`). `Pq` y `M` **no** se heredan: el código no existe en el individuo.

## 5. Criterios

### 5.1 Instrumento (paran la corrida)
- **K1a [tronco]:** `mundo_social_n3.run(n=1, mundo='regla', regla='azar', regen=None)` ≡ `organismo_v13g` (tronco,
  `fase2_en=0`, `eta_s=0.015`, `puerta=3`) en `W, mord, vis, deaths, splits, split_t, celdas`, semillas 1–3.
- **K1b [vía de símbolos]:** `mundo_social_n3.run(n=2, senal='simbolo', regen=None, **perillas)` ≡ `mundo_social.run(…)`
  en **todas** las claves de `mundo_social`, semillas 1–3. (Las dos perillas N2f apagadas; su identidad con `regen=50`
  ya está verificada aparte, §2.)
- **K2 [canal]:** en CONV el novato recibe ≥ **1.000** símbolos (mediana).

### 5.2 Validez del mundo (pueden fallar; son las que mataron la v1)
- **K3 [queda algo que enseñar]:** en SOLO, el novato muerde veneno en el **último cuarto ≥ 20** veces (mediana).
  Con rotación deberían aparecer patrones nuevos toda la corrida; si aun así el novato ya no se equivoca, el montaje es
  **inválido** (S4 de N3c) y E1–E5 se reportan pero no cierran ni refutan nada.
- **K4 [visitas equilibradas]:** en CONV, emisiones del experto en estado "muerde" ≥ **1/5** de las de "rechaza"
  (N2d: 1/64) **y** el novato oye ≥ **500** símbolos de estado "muerde" (N2d: 113).
- **K5 [el mundo con `vida` todavía se puede aprender] — puerta propia de la tercera perilla.** `vida` corta por el
  otro lado: si el mundo se renueva demasiado rápido, el novato no llega a consolidar nada por su cuenta y el montaje
  vuelve a ser inválido, ahora por exceso. Operacionalización: **en SOLO, `veneno_q4 < veneno_q1` en ≥ 15/20**.
  K3 y K5 son una **tenaza**: K3 dice "que no sea tan fácil que ya lo sepa todo" (sigue equivocándose en Q4) y K5 dice
  "que no sea tan difícil que no aprenda nada" (se equivoca menos al final que al principio). `vida` se elige por
  K3+K4+K5 y **nunca** por E1–E5.

### 5.3 Científicos — **E1–E6 verbatim de N2/N2b, sin suavizar un umbral**, evaluados en **CONV**
- **E1 [convención]:** el experto termina con estados que prefieren **símbolos distintos** y consistencia Q4 ≥ **0.9**,
  en ≥ **15/20**.
- **E2 [decodificación]:** `C[s_rech] ≤ −1.0` **y** `C[s_mord] ≥ +0.3` en ≥ **15/20**, con `C[s] = M[s] − media(M)`.
- **E3 [arbitrariedad]:** "rechazo" es el símbolo `0` en **entre 5 y 15** de las 20 semillas.
- **E4 [beneficio]:** veneno propio del novato en CONV ≤ **0.7 ×** N0 (mediana) **y** CONV < N0 pareado en ≥ **14/20**.
- **E5 [muere al barajar]:** en SHUF, `|C[s]| < 1.0` para los dos símbolos en ≥ **15/20**, y veneno ≥ **0.9 ×** N0.
- **E6 [no existe en el individuo]:** SOLO no tiene símbolos; se reporta y no vota.
- **Réplica:** si E1–E5 pasan en 81–100, se repiten en **101–120**; sólo entonces se escribe "N2 cerrado".

### 5.4 Atribución — **criterios nuevos, y digo por qué**: CONV_MUNDO separa las dos perillas
Sin este brazo no se puede saber cuál de los dos cambios hizo el trabajo, y el proyecto ya pagó ese precio en N2c/N2d
(dos hipótesis sobre el emisor refutadas por no tener brazo de atribución).
- **A1 [la magnitud la da el MUNDO]:** E2 se cumple también en **CONV_MUNDO** (≥ 15/20). *Si A1 pasa, la magnitud viene
  de la rotación y no de la puerta del receptor.*
- **A2 [el beneficio necesita la PUERTA]:** E4 pasa en **CONV** y **no** en CONV_MUNDO. *Si pasa en los dos, la puerta
  sobra y se registra así; si no pasa en ninguno, manda otra cosa (§6).*
- Se reporta `no_desensena` (cuántas veces la puerta bloqueó el empujón) y `decodificados` en los dos brazos.

## 6. Predicción numérica (escrita antes de correr)

- **K3 pasa** (la rotación mete patrones nuevos toda la corrida). Es lo primero que hay que mirar.
- **K4 pasa** (la v1 ya dio 0.286; la rotación no empeora el reequilibrio).
- **E2 pasa en CONV y en CONV_MUNDO** (A1 ✅): la magnitud viene del mundo. La v1 ya dio ±1.28 con una sola semilla.
- **E4 pasa SÓLO en CONV** (A2 ✅): el beneficio necesita no desenseñar. En CONV_MUNDO espero repetir el daño de la v1
  (CONV peor que N0).
- **E1 ≥ 15/20**, **E3 ≈ 10/20**, **E5 sostenida**.
- **P1/P2 del bloque 5 del plan** (contraste `|C| ≥ 0.5` en ≥ 10/20; beneficio ≥ 1.2 × N0 en ≥ 15/20) se reportan como
  marca de progreso; **no sustituyen a E2/E4**, que son más exigentes.
- **Incertidumbre honesta:** con rotación el novato ve muchos más patrones y el experto conocía sólo 6 de 10 venenos a
  200k; sobre los que no conoce emitirá "muerde" con confianza (el fenómeno de N2c/N2d). Eso puede hundir E4 en los dos
  brazos aunque E2 pase.

## 7. Refutación

- **E4 falla en CONV y en CONV_MUNDO, con K1–K4 en pie:** el beneficio no llega ni con visitas equilibradas, ni con
  flujo de patrones, ni con un receptor que no se deja desenseñar. Entonces **manda la causa que queda declarada desde
  N2e: la escala asimétrica (−3 / +1)**, y N2 queda cerrado con **dos mundos** y tres receptores. No se reabre sin
  cambiar la escala y sin preregistro nuevo.
- **E4 pasa en los dos brazos:** la puerta sobra; el hallazgo es del mundo, y se registra sin adornos.
- **E2 falla con K3/K4 pasando:** la magnitud de la v1 (±1.28) era un artefacto del mundo congelado de 5 patrones, y se
  registra así (es la sospecha que dejé escrita en la enmienda de la v1).
- **K3 o K4 fallan:** montaje inválido otra vez; se registra el mundo, no el organismo.
- **Nada se recalibra después de ver los datos.** Un séptimo diseño sólo con ERR numerado, criterio nuevo y semillas
  nuevas.

## 8. Las cuatro trampas, revisadas

1. **Canal social simétrico (ERR-23).** Sigue siendo simétrico y **declarado**: los dos organismos emiten, los dos
   oyen y `escucha_si_no_sabe` vale para los dos. Es el montaje de N2; lo que se lee es el `Pq` del experto y la `M` del
   novato. Cambiarlo sería otro experimento.
2. **Acierto sin balancear.** No se usa "acierto": todo son conteos (veneno propio, emisiones, `M`, `Pq`,
   `no_desensena`) y E4 es pareado CONV contra N0 en la misma semilla. *Riesgo vivo:* un novato que muerde poco baja el
   veneno sin saber nada; por eso se reportan comidas conocidas, muertes y `venenos_conocidos` **restringidos a los
   patrones presentes**.
3. **Mundo que se come la comida.** Medido en la v1: `regen` lo reduce ×18 pero **no lo elimina** (por objeto ~7 : 1,
   porque el veneno rechazado no se retira nunca). La rotación no cambia eso; K4 lo vigila con un umbral (≥ 1/5) que
   admite asimetría residual y **el humo vuelve a contar emisiones por estado**.
4. **Sitios fijos que se memorizan.** Es **la trampa que mató la v1** y la que `regen_rota` ataca de frente: los sitios
   siguen fijos, pero **el tipo que aparece en ellos ya no**, así que no se puede memorizar "sitio → valencia". Se
   verifica con dos medidas: **patrones presentes** (debe subir de 5 hacia ~20) y **K3**.

## 9. Qué se decide

- **K1–K4, E1–E5 y réplica:** *"entre dos organismos v13, en un mundo que devuelve lo mordido con un tipo nuevo, emerge
  un código de dos símbolos que ninguno tenía, arbitrario por semilla, con magnitud útil, que reduce el veneno y que
  muere al barajarlo"*. N2 cerrado. Vocabulario: *emerge, transmite*. **No** "lenguaje", **no** "entiende".
- **A1/A2** dicen **a qué** atribuirlo: al mundo, a la puerta del receptor, o a los dos.
- **K3 o K4 caen:** montaje inválido; se registra el mundo, no el organismo.

---

## ENMIENDA 1 (día 6; escrita TRAS el humo de la v2 y ANTES de correr las 20 semillas)

Mismo protocolo que la ENMIENDA 1 de `PREREGISTRO_N2.md`. **No se toca ningún umbral.** Humo:
`corre_N2f.py --humo --semilla 81`, un proceso: progenitor + N0 + CONV + CONV_MUNDO (4 × 200k) más K1a/K1b.
Datos `datos/N2f_humo_s81_20260917_215823.json` (`20eeb5fda099aef1`).

**K1a y K1b: IDÉNTICOS.** **K3: pasa** (proxy sin SOLO: veneno Q4 del novato en N0 = **43** ≥ 20; **20 de 20 patrones
presentes**; venenos conocidos 9/10, comidas 8/10). La rotación arregla lo que mató a la v1.

**Pero K4 FALLA, y por una causa nueva que ningún diseño anterior había visto.**

| | v1 `regen=50` sin rotación | **v2 `regen=50` + rotación** | N2d (mundo original) |
|---|---|---|---|
| patrones presentes | 5 | **20** ✅ | 20 |
| veneno Q4 del novato (N0) | 3 ❌ | **43** ✅ | — |
| emisiones rechaza / muerde | 19.335 / 5.524 (**0.286**) ✅ | **36.201 / 794 (0.022)** ❌ | 36.365 / 564 (0.016) |
| visitas comida/veneno por cuarto (experto) | 0.296 · 0.285 · 0.283 · **0.272** (plana) | **0.037 · 0.021 · 0.015 · 0.018** (decae) | — |
| contraste `C[s]` | ±1.28 | **±0.30** | ±0.34 |
| `s_rech` ≠ `s_mord` | sí | **no** (los dos = 0) | — |

**Causa, medida: el mundo se absorbe en veneno.** Un objeto sólo se retira **cuando se muerde**. La comida se muerde,
se retira y, con rotación, vuelve con un **tipo nuevo**; el veneno se rechaza y **no se retira nunca**. Cada sitio que
saca veneno se queda con veneno para siempre: es una **cadena absorbente**. La razón comida/veneno **decae cuarto a
cuarto** (0.037 → 0.015) y termina en 1 : 44, que es exactamente la asimetría del mundo original de N2.

**Reinterpretación obligada de la v1 (y de la frase "`regen` equilibra visitas"):** el reequilibrio ×18 de la v1 **no
lo daba la reaparición en sitio**, lo daba la **congelación** — los 8 objetos del sorteo inicial eran 3 comidas y 2
venenos, y esa composición no podía degradarse. Reaparición en sitio y flujo de patrones, con esta regla de retirada,
**son incompatibles**: el que da balance congela el mundo, y el que da flujo lo absorbe en veneno.
(En N3c/N3d el problema no salió porque allí el mundo es de 8 objetos fijos por diseño, sin rotación.)

**Consecuencia sobre los brazos:** con `|C| = 0.30 < u_m = 1.0` la puerta vicaria **nunca abre** (`decodificados = 0`,
`no_desensena = 0`), así que **CONV y CONV_MUNDO salen bit a bit iguales** y A1/A2 no pueden medir nada. La perilla
`escucha_si_no_sabe` está bien construida y verificada, pero **en este mundo no tiene ocasión de actuar**: sólo actúa
cuando el símbolo tiene magnitud, y la magnitud sólo apareció en el mundo congelado.

**Predicción de §6 revisada por los hechos, sin recalibrar:** acerté K3 y E4-incierto; **fallé en K4** (predije que la
rotación no empeoraría el reequilibrio: lo destruye). Queda escrito como fallo de mi predicción.

**Lo que falta, cuantificado (probe de dinámica del mundo, sin organismos, `scratchpad/probe_absorcion.py`; un
paseante que muerde comida y rechaza veneno):** hace falta que **el veneno también salga del mundo**, es decir una
**vida máxima por objeto** (`vida`: el objeto caduca y se regenera aunque no se muerda). Razón comida/veneno medida:

| mundo | razón comida/veneno |
|---|---|
| v1 (regen 50, sin rotación) | 0.366 |
| **v2 (regen 50 + rotación)** | **0.015** |
| + `vida = 500` | 0.073 |
| + `vida = 200` | 0.140 |
| **+ `vida = 50`** (= `regen`) | **1.010** |

Es **una** perilla más en `Mundo`, del mismo tipo que `regen_rota` y anclable igual, con `vida=None` idéntico a lo
actual. **No se construye aquí:** es un tercer diseño y lo arbitra el coordinador. **Riesgo declarado del candidato:**
con `vida ≈ 50` el mundo cambia entero cada 50 pasos y puede que el novato no llegue a aprender nada por su cuenta
(K3 al revés: demasiado que enseñar y ningún tiempo para aprenderlo); habría que elegir `vida` con su propia puerta de
validez, no por la razón de visitas sola.

**Recomendación al coordinador: NO gastar el `Pool` en la v2 como está** (K4 cae por construcción y los dos brazos de
símbolos son idénticos, así que las 120 corridas no pueden distinguir nada). Las dos perillas quedan construidas,
verificadas (identidad 8/8) y listas para el diseño que añada `vida`.

---

## ENMIENDA 2 (día 6; **`vida` queda FIJADO EN 100 por el humo**, antes de correr las 20 semillas)

El coordinador aceptó la tercera perilla. `vida` está construida por anclas, `mundo_social_n3.py` regenerado
(`ef227f833c5bf46a`) e **identidad 8/8** con las tres perillas apagadas (incluidos N3c/N3d). El barrido pedido
(`corre_N2f.py --humo --semilla 81`; progenitor + N0 + CONV por cada `vida`, 200k; datos
`datos/N2f_humo_vida_s81_20260917_221553.json`, `940fb8cf84ae6b36`) da:

| `vida` | patrones presentes | rechaza/muerde (razón) | visitas comida/veneno por cuarto | **K4** (≥ 0.200) | **K3** proxy (veneno Q4 en N0 ≥ 20) | **K5** proxy (Q4 < Q1) | caducados |
|---|---|---|---|---|---|---|---|
| **50** | 20 | 13.733 / 5.038 (**0.367**) | 0.41 · 0.41 · 0.36 · 0.33 (plana) | ✅ | ✅ 259 | ❌ **172 → 259 (sube)** | 8.651 |
| **100** | 20 | 17.657 / 4.645 (**0.263**) | 0.32 · 0.28 · 0.27 · 0.27 (plana) | ✅ | ✅ 49 | ✅ **167 → 49** | 6.270 |
| **200** | 20 | 24.129 / 3.146 (**0.130**) | 0.16 · 0.14 · 0.12 · 0.12 (decae) | ❌ | ✅ 62 | ✅ **174 → 62** | 4.049 |

**`vida` = 100: el único que pasa K3, K4 y K5 a la vez.** `vida = 50` renueva tanto el mundo que el novato **empeora**
(muerde más veneno al final que al principio: K5 lo rechaza). `vida = 200` deja que el veneno se acumule otra vez y la
razón vuelve a decaer cuarto a cuarto: K4 lo rechaza. La tenaza K3/K5 funcionó tal como se escribió.

**Y hay que decirlo con todas las letras, porque es lo que protege este preregistro de una trampa:** en la semilla del
humo, **el `vida` que gana por las puertas NO es el que mejor resultado da**. Con `vida = 50` el contraste sale
**±1.12** con convención perfecta (consistencia 1.000, símbolos distintos) y CONV mejora a N0 (582 contra 691); con
`vida = 100` **no hubo convención** en esa semilla (`distintos = False`, `s_rech = s_mord = 0`, contraste ±0.23,
`decodificados = 3`) y CONV salió peor que N0 (455 contra 327). **Elegir 50 sería elegir por el resultado**, que es
exactamente lo que el método prohíbe. Se fija **`vida = 100`** por K3+K4+K5, escrito aquí antes de correr, y
`corre_N2f.py` lo lleva fijado (`VIDA = 100`).

**Aviso, no recalibración:** esa semilla sugiere que E1 y E2 pueden caer en las 20 semillas. **La predicción de §6 se
queda como está escrita**; este párrafo es el aviso, y si cae se registra como refutación con la causa a la vista.
Una semilla no decide nada: `vida = 50` también dio un mundo donde el novato no aprende, y ahí un símbolo puede
"parecer" útil precisamente porque el receptor no tiene nada propio con que competir — otra razón para no elegirlo.

**Límite declarado del humo:** K3 y K5 se midieron con el **proxy de N0** (novato + experto sin señal), no con SOLO,
porque SOLO no cabía en el presupuesto de un proceso. En la corrida de 20 semillas se evalúan sobre **SOLO**, como dice
§5.2, y pueden caer ahí.
