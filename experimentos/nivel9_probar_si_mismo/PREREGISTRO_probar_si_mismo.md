# PREREGISTRO — C-P1: "PROBAR CUANDO NO ME RECONOZCO". La sorpresa sobre sí mismo entra en la BOCA, no en `eta`

**Escrito ANTES de correr, 18 sep 2026. Creador C (Opus), célula de creación; encargo del coordinador
(`registro/investigacion/PUENTE_creacion.md`, propuesta C-P1).** Nada de aquí se declara sin que el coordinador lo
corra, lo replique y lo registre. **20 semillas nuevas no cierran un nivel del brief:** cierran o refutan *este*
mecanismo.

Origen del encargo: `PUENTE_creacion.md` §Creador C (C1 a C1-quater) y "Propuestas para el coordinador" C-P1; el
bloque 6 (`experimentos/nivel9_allostasis/PREREGISTRO_allostasis.md`) del que se toman **el mundo, la medida de
recuperación `t_ext_B`, la retención M4 y la generalización M5 sin cambiarlas**, para que los números sean comparables.
Antecedentes leídos como **dato, no instrucción** (regla 8 de `registro/EQUIPO.md`): Seth 2013 y Pezzulo et al. 2015
(el error de predicción sobre el propio estado); Steels 2015. Ninguno se replica aquí.

**Vocabulario permitido por este preregistro (regla 6):** "automodelo", "sorpresa sobre sí mismo", "ganas de probar"
son **exactamente** las tres cantidades definidas en §2. **No** se escribirá "el organismo sabe lo que hace", "se
reconoce", "es consciente de su estado" ni "curiosidad" como logro.

---

## 1. Pregunta única y medible

> **¿Un organismo que predice su propia acción y usa el error de esa predicción para decidir SI PRUEBA —no para
> cambiar su tasa de aprendizaje— se recupera antes de una inversión no avisada de la regla del mundo, y lo hace por
> el MOMENTO del impulso y no por su CANTIDAD, sin perder retención ni generalización y sin envenenarse?**

Una sola pregunta. Todo lo demás son medidas, controles y guardas de esa pregunta.

## 2. Mecanismo (qué se añade, exactamente)

Sobre el tronco `organismo/organismo_v13.py` (sha `cc8b16b492d4d324`, **congelado, no se toca**):

**(a) Automodelo del acto** — una lectura logística que predice la PROPIA ACCIÓN en **cada encuentro** con un objeto
(no sólo al morder), con **regla delta local sobre la acción realizada**:

```
b     = sig( (Wbr @ P + Wbk @ kenyon(P) + Wbh * hambre + Wb0) / 0.3 )
e_b   = mordio - b                      (mordio en {0,1}, la accion que el organismo acaba de tomar)
Wbr  <- clip(Wbr + eta_b * e_b * P,          +-clip_b)
Wbk  <- clip(Wbk + eta_b * e_b * kenyon(P),  +-clip_b)
Wbh  <- clip(Wbh + eta_b * e_b * hambre,     +-clip_b)
Wb0  <- clip(Wb0 + eta_b * e_b,              +-clip_b)
```

**(b) Sorpresa sobre sí mismo y su promedio.** `s_a = |mordio - b|` en cada encuentro, y
`s̄_a <- (1 - ema_auto) * s̄_a + ema_auto * s_a`. **`s̄_a` es CAUSAL**: se actualiza *después* de leer la acción, así que
la boca del encuentro *n* usa el promedio de los encuentros 1…*n−1*. Es lo único que hace falta para que el mecanismo
no vea el futuro, y es comprobable en la identidad J2.

**(c) El uso, y es el punto del bloque: entra en la BOCA, no en `eta`.**

```
Vb = alpha * w + hambre_boca * hambre + 0.5 + k_test * s̄_a
```

`eta` **no se toca** (la perilla `k_auto` existe en el instrumento pero va en **0 en todos los brazos**). Tampoco se
toca `valor()`, ni la vía lenta, ni las patas, ni el mapa: **no se añade ninguna atracción**, y por eso este bloque no
repite los tres candidatos ya refutados del canje exploración/explotación (curiosidad por progreso, novedad de sitio
en dos dosis).

**Por qué en la boca y no en `eta`, escrito antes:** el cuello de la recuperación tras una inversión **no es la tasa,
es cuántas veces muerde**. El bloque 6 lo mostró por el lado contrario: la sorpresa de ΔE modulando `eta` con k = 1
dio 0.856 × el tiempo de v13 (pareado 6/10), es decir casi nada.

**Memoria que exige:** 6 + `NKMAX` + 2 = **98 escalares** (una lectura lineal del tamaño de la vía lenta, más una copia
sobre el pool de celdas, más el peso del hambre y el sesgo) **+ UN escalar de estado** (`s̄_a`). **Nada por objeto,
nada por sitio, nada episódico, ningún almacén** — la trampa "memoria escondida" (K4 de la Etapa 4) no aplica: no hay
dónde esconderla.

**Perillas y sus valores, ninguno buscado después de ver datos:**

| perilla | valor | de dónde sale |
|---|---|---|
| `eta_b` | **0.03** | **el mismo `eta` del tronco**. Además, elegido por la **regla de método** de §10 bis: entre 0.03 y 0.3, gana el que da menor pérdida al **brazo de CONTROL**, no al de la hipótesis (0.0672 contra 0.0886) |
| `ema_auto` | **0.05** | igual que el `ema` de la instrumentación del tronco (0.02) en orden de magnitud; ventana efectiva ≈ 20 encuentros ≈ 200 pasos |
| `k_test` | **10** | **fijado ANTES por la escala medida**, no por el resultado: `s̄_a` ≈ 0.004 (régimen) → 0.020 (tras el cambio), luego el término vale ≈ 0.04 → 0.20 en unidades de `Vb`, que se divide por 0.3. Es el valor de la mini-prueba de C-P1 y **no se mueve** |
| `buf_auto` | **1000** encuentros | ventana del control H_SHUF de las lecturas; ≈ 10 000 pasos, **muy por encima** del tiempo de autocorrelación del hambre (ver §10 bis, nota de método) |
| `clip_b` | 3.0 | el `clip_s` del tronco |
| `k_auto` | **0** en todos los brazos | este bloque **no** modula `eta` |

## 3. Instrumento

**Linaje, con sha y con identidad bit a bit en cada eslabón:**

```
organismo/organismo_v13.py                      cc8b16b492d4d324   TRONCO CONGELADO (se lee, no se toca)
  -> experimentos/creacion_C/organismo_v13s.py  2eaba8dde27f05bd   automodelo + k_test + test_fijo      [I1/I2/I3 = 18/18]
       constructor: experimentos/creacion_C/construye_selfmodel.py  27c91df159a1465b
  -> experimentos/nivel9_probar_si_mismo/organismo_v13p.py   0dbc2495efe44e60   + dE en la boca, traza MOMENTO, mord_post
  -> experimentos/nivel9_probar_si_mismo/organismo_v13pg.py  7ab4767d446ba797   idem desde organismo_v13g.py (2a80e125f8593bf2), mundo de regla
       constructor: experimentos/nivel9_probar_si_mismo/construye_probar.py
```

Los bloques del automodelo **se importan** de `construye_selfmodel.py`, no se copian: el código que corre aquí es,
byte a byte, el que pasó I1/I2/I3. **Ningún generado se edita a mano.**

## 4. Identidades (se corren PRIMERO, DENTRO del runner; si fallan, el runner aborta y no hay experimento)

- **J1 — apagado ≡ tronco:** `organismo_v13p.run(todo apagado)` == `organismo_v13.run(...)` en **todas las claves de
  v13**, semillas 1–3 × 3 escenarios {base, `invertir_en=T/2`, `nuevo='C'`}.
- **J2 — las lecturas SÓLO MIDEN:** `organismo_v13p.run(eta_b=0.03, ema_auto=0.05, eta_e=0.05, eta_pred=0.03,
  ema_pred=0.05, n_traza=2000, k_test=0, k_testE=0, k_auto=0)` == `organismo_v13.run(...)`, mismas semillas y
  escenarios. **Es la identidad que da derecho a llamar "medida" a todo lo que este bloque lee**, y la que comprueba
  que `s̄_a` es causal: si la boca viera la acción del propio encuentro, J2 no podría ser idéntica.
- **J3 — continuidad con la mini-prueba:** `organismo_v13p.run(brazo SELF-TEST)` == `organismo_v13s.run(el mismo
  brazo)`. Garantiza que los números de C-P1 en el puente son los de este instrumento.
- **J4 — modo regla:** `organismo_v13pg.run(todo apagado, mundo='regla')` == `organismo_v13g.run(...)`, px0 y azar.

**Ya comprobadas por el diseñador, un proceso, T = 5 000:** **J1 18/18 · J2 18/18 · J3 18/18 · J4 6/6.** El runner las
vuelve a correr (las tres primeras a T = 10 000) antes de tocar nada.

## 5. Brazos, mundo y semillas

| brazo | perillas | qué es |
|---|---|---|
| **V13** | — (todo apagado) | el tronco, línea base |
| **SELF-TEST** | `eta_b=0.03, ema_auto=0.05, k_test=10, buf_auto=1000, n_traza=2000` | **la hipótesis** |
| **CONST-a** (control de cantidad) | `test_fijo=0.173` | sesgo **constante** = la **media** del sesgo que SELF-TEST aplicó en la mini-prueba |
| **CONST-b** (control de cantidad) | `test_fijo=0.31` | sesgo **constante** = el **nivel que SELF-TEST alcanza en Q3**, el cuarto que decide. Es el control **más duro**: da el nivel bueno todo el rato |
| **MOMENTO** (control de momento) | `k_testM=10, desfase=500`, `traza_ext` = la traza de SELF-TEST **de esa misma semilla** | **exactamente la misma cantidad de sesgo, fuera de tiempo** (ver abajo) |
| **dE-TEST** (exploratorio, **no** es criterio) | `eta_pred=0.03, ema_pred=0.05, k_testE=10` | la sorpresa de **ΔE** del bloque 6 entrando en la **boca** con la **misma ganancia**: separa *qué* sorpresa de *dónde* entra |

**MOMENTO, definido exactamente (y por qué un cuarto y no la mitad).** Durante SELF-TEST se registra `traza_s[i]` = la
media de `s̄_a` en la cubeta *i*, con `n_traza = 2000` cubetas de `T/n_traza = 100` pasos. En MOMENTO, el sesgo del paso
*t* es `k_testM · traza_s[(i + desfase) mod n_traza]` con `i = t·n_traza/T` y **`desfase = n_traza/4 = 500` cubetas =
50 000 pasos = un cuarto de la corrida**. Un desplazamiento circular **conserva la suma exactamente**: MOMENTO aplica
el mismo sesgo total que SELF-TEST, minuto a minuto distinto. **Por qué un cuarto y no la mitad:** con medio T el pico
de aprendizaje de Q1 caería **justo sobre la inversión** y MOMENTO dejaría de ser un control de *momento equivocado*
(llevaría un pico grande exactamente donde ayuda). Con un cuarto, el pico de Q3 se va a Q4 y Q3 recibe el nivel bajo
de Q2. **Escrito antes de correr.** El instrumento no usa RNG para esto: el control es determinista.

**Mundo:** el anillo del tronco, escenario del bloque 6: **`T = 200 000`, `invertir_en = 100 000`** (= T/2). Los
cuartos quedan alineados con el evento: Q1, Q2 antes; Q3, Q4 después.

**Semillas: 41–60** (20, **nuevas para este mundo**: el bloque 6 usó 1–10 y la mini-prueba de C-P1 usó 1–3). El
diseñador **no ha visto** ninguna semilla ≥ 41 en este mundo. **Declaración de exposición:** las semillas 1–3 se
vieron enteras en la mini-prueba y las 1–6 en las identidades (donde por construcción no hay nada que ver).

**Retención (M4) y generalización (M5) se corren para V13, SELF-TEST y CONST-b**, no para los seis brazos: P5 y P6
preguntan si **la hipótesis** daña algo, y CONST-b es la referencia de control. **MOMENTO no puede correrse en las
baterías** (necesita la traza de una corrida de este mundo, que allí no existe) y dE-TEST es exploratorio. Declarado
aquí para que no se lea después como una omisión.

## 6. Medidas

Del tronco: `W`, `comp`, `mord`, `vis`, `deaths`, `splits`, `celdas`, `W_lenta`.

- **M1 `t_ext_B`** — primer paso `t >= invertir_en` con `valor('B') >= 0`, **el criterio exacto del bloque 6** (que a
  su vez es el de `mundo_social.py`, líneas 156–157). **Censurado = `T`** si nunca ocurre. Se informa
  `recup = t_ext_B - invertir_en`.
- **M2** `mord_post` separado en `comida` / `veneno`, y `deaths_post`.
- **M3 `sesgo_boca[q]`** — media, por cuarto, del sesgo que el brazo aplicó realmente a `Vb`. **Es la medida que
  convierte "cantidad contra momento" en dos números**, y se informa para los seis brazos.
- **M4 `sorpresa_auto[q]`**, `encuentros[q]`, `auto_ll` / `auto_ba` dentro y fuera de la banda derivable
  `w ∈ [(−0.9−0.5−hambre_boca)/alpha, (0.9−0.5)/alpha] = [−2.8333, +0.3333]`, con el **ORÁCULO** (la propia `pb`) como
  cota irreducible. Diagnóstico, no criterio.
  **Aviso de lectura, escrito antes de correr:** las cifras de la banda **no son comparables entre brazos que cambian
  la política**. En el humo, SELF-TEST deja sólo **151** encuentros dentro de la banda (V13 en la mini-prueba tenía
  6 154), porque muerde más, consolida antes y su `w` pasa menos tiempo ahí. La banda sirve para leer **un** brazo, no
  para comparar dos con conductas distintas; no se usará para ningún criterio de este bloque.
- **M5 retención** — las SEIS etapas de `organismo/bateria_v13.py` (`E1, E2, E2I, E2J, E2K, E2L`, T = 100 000) con sus
  `CRIT` **importados tal cual**. No se reescribe ningún umbral.
- **M6 generalización** — G1/G2 px0/azar con `organismo_v13pg.py`, reproduciendo **literalmente** la fórmula de
  `organismo/bateria_generaliza.py` (`46772f5a582872c8`) como ya hace el runner del bloque 6. **No se modifica**
  `bateria_generaliza.py`.

## 7. Predicción numérica (escrita antes de correr; no se recalibra)

Semillas 41–60, `T = 200 000`, `invertir_en = 100 000`. Entre paréntesis, lo que dio la mini-prueba en 1–3.

- **P1 [acelera]** — mediana de `recup` de **SELF-TEST ≤ 0.60 ×** la de **V13**, y pareado (SELF-TEST más rápido en la
  misma semilla) en **≥ 14/20**. *(mini-prueba: 0.315 ×, 3/3.)*
- **P2 [no es la CANTIDAD]** — SELF-TEST más rápido que **CONST-a** en **≥ 14/20** pareado **y** que **CONST-b** en
  **≥ 14/20** pareado. *(mini-prueba: 3/3 contra cada uno.)*
- **P3 [es el MOMENTO]** — SELF-TEST más rápido que **MOMENTO** en **≥ 14/20** pareado. *(no medido en la mini-prueba:
  el control no existía.)*
- **P4 [se apaga solo]** — `sesgo_boca[Q2] ≤ 0.10` y `sesgo_boca[Q4] ≤ 0.10` **y** `sesgo_boca[Q3] ≥ 0.20`, en
  **≥ 16/20**. *(mini-prueba: Q2 0.063–0.068, Q4 0.044–0.060, Q3 0.260–0.366.)*
- **P5 [no daña la retención]** — en **cada una** de las SEIS etapas, SELF-TEST pasa en **≥ 18/20** semillas.
- **P6 [no daña la generalización]** — G1 px0 de SELF-TEST **≥ 0.80** en mediana (el número del bloque 6 y de la
  batería registrada de v13) y **≥ mediana(V13) − 0.10**; control `azar` en **[0.35, 0.65]**.
- **P7 [probar no es envenenarse]** — mediana de `veneno_post` de SELF-TEST **≤ 4 ×** la de V13 **y** mediana de
  `deaths` **≤ 1.50 ×** la de V13. *(mini-prueba: veneno 3.4–3.9 ×; muertes 1.01–1.28 ×.)*

**Diagnóstico exploratorio, sin criterio (dE-TEST):** se informan `recup` y `sesgo_boca[q]` de dE-TEST junto a los de
SELF-TEST. Lectura preregistrada: si dE-TEST iguala o bate a SELF-TEST **con un sesgo mayor**, lo que importa es
**dónde entra** la sorpresa, no cuál; si pierde **teniendo un sesgo mayor**, importan las dos cosas. En ningún caso
cambia el veredicto del bloque.

## 8. Criterio de refutación (explícito, cláusula por cláusula)

- **P1 falla** → **REFUTADO**: la sorpresa sobre sí mismo en la boca no acelera la recuperación. Se registra así, **sin
  reintentos con otro `k_test`** (eso sería un experimento nuevo, con preregistro y semillas nuevas).
- **P1 sí, P2 no** → lo que acelera es **la cantidad de sesgo**, no la sorpresa. Se registra con ese nombre y el
  mecanismo queda reducido a "morder más".
- **P1 y P2 sí, P3 no** → lo que acelera es **el nivel del sesgo**, no el momento: la traza desplazada sirve igual.
  Se registra así y el mecanismo pierde su razón de ser (deja de ser "cuando no me reconozco").
- **P7 falla** → **NULO**: "probar" es "envenenarse"; M1 no mide lo que dice y el contraste se anula.
- **P4 falla** → el lazo *sorpresa → morder → sorpresa* **se autoamplifica**: el mecanismo no tiene apagado. Se
  registra como límite medido aunque P1–P3 pasen.
- **P5 o P6 fallan** → acelera **a costa** de retención o generalización: es un **canje medido**, no una mejora (el
  proyecto ya tiene tres: puerta/capacidad, mapa/adquisición, exploración/explotación).
- **Todo pasa** → *"la sorpresa sobre su propia conducta, puesta en la boca, le hace probar justo cuando deja de
  predecirse, y por eso se recupera antes de un cambio no avisado"*, **y pide réplica preregistrada en semillas nuevas
  (61–80) antes de cualquier afirmación**. No es un tronco nuevo ni un nivel del brief cerrado.

## 9. Guardas de validez (se miran ANTES que las predicciones; si una cae, el contraste es nulo y va ERR numerado)

- **G-a [identidades]** J1, J2, J3, J4 al 100 %. Si no, el runner **aborta** (no se corre el experimento).
- **G-b [la cantidad se ve, no se supone]** se informa `sesgo_boca[q]` de los seis brazos y la **razón**
  `sesgo_boca[Q3](CONST-b) / sesgo_boca[Q3](SELF-TEST)` y `sesgo_boca[Q3](MOMENTO) / sesgo_boca[Q3](SELF-TEST)`.
  Lectura preregistrada de P2/P3, como en la ENMIENDA 1 del bloque 6:
  - razón ≥ 1.0 → contraste **limpio y fuerte** (el control recibió igual o más y aun así fue más lento);
  - 0.95 ≤ razón < 1.0 → contraste **válido**;
  - razón < 0.95 → **INCONCLUSO**, candidato a ERR: la ventaja está confundida con "más sesgo".
- **G-c [hay sitio para acelerar]** mediana de `recup` en **V13** entre **500** y **T/2 − 1** pasos, y censuradas
  (`t_ext_B is None`) en **≤ 4/20**. Si V13 se recupera en menos de 500 pasos no hay margen; si no se recupera nunca,
  la medida está censurada. En ambos casos M1 no sirve y hace falta otro mundo (ERR).
- **G-d [la traza de MOMENTO conserva la masa]** `|suma(traza inyectada) − suma(traza de SELF-TEST)| < 1e−9` por
  semilla (es un desplazamiento circular: debe ser exacto). Si no, el control está mal construido.

## 10. Trampas revisadas (regla 5 de `CLAUDE.md`, §6 de `nivel9_autonomia.md`, y las cuatro de la noche del 17-sep)

| trampa | cómo se evita aquí |
|---|---|
| **"más sesgo" confundido con "el sesgo correcto"** | DOS controles de cantidad (CONST-a media, CONST-b nivel de Q3) **y** uno de momento (MOMENTO), con `sesgo_boca[q]` medido, no supuesto (G-b) |
| **premiar pasividad** | P7 por un lado (veneno) y P1 por el otro; además se informa `comida_post` |
| **premiar temeridad** (la trampa inversa, que es la de este mecanismo) | P7 exige muertes ≤ 1.50 × V13: si "probar" es "morir", el brazo cae |
| canal social simétrico | no hay canal social en este bloque |
| acierto sin balancear | M1 es un **tiempo**, no un acierto; G1/G2 vienen ya balanceados de `bateria_generaliza` |
| mundo que se come la comida | mundo del tronco sin tocar, `nobj = 4` con reposición; los brazos difieren **sólo** en las perillas nuevas |
| sitios fijos que se memorizan | no se usan sitios; la inversión es de valencia, no de posición |
| memoria escondida (K4) | la memoria del mecanismo son 98 escalares + 1; no hay almacén ni nada por objeto o por sitio |
| Goodhart | ninguna medida de aquí entra en un criterio de aceptación de EVO ni de tronco: es una rama |
| criterio que no puede fallar | P1–P7 pueden fallar; G-a aborta; G-b y G-c pueden anular el contraste; J2 puede refutar que las lecturas "sólo miden" |
| declarar por conducta compleja | vocabulario tasado en la cabecera |

## 10 bis. Nota de método, y un ERR candidato que el diseñador halló y corrigió antes de este preregistro

1. **ERR candidato — "control demasiado débil" (familia nueva).** Al construir el automodelo, el control que baraja el
   hambre en el tiempo usaba una ventana de **10 encuentros (≈ 100 pasos)** y **aprendía el hambre casi igual que el
   brazo de la hipótesis** (`Whh` = 0.487 contra `Wbh` = 0.788): **barajar dentro de una ventana más corta que el
   tiempo de autocorrelación de la variable no la baraja.** Con 1 000 encuentros (≈ 10 000 pasos) el control colapsa a
   `Whh` = −0.003. Aquí `buf_auto = 1000` por esa razón. **Regla derivada, propuesta para el protocolo:** *todo control
   de barajado debe declarar la ventana y justificarla contra el tiempo de autocorrelación de lo que baraja* — el
   control de RUIDO del bloque 6 (`buf_sorpresa = 10` bocados) debería revisarse con este criterio.
2. **Regla para que la tasa de una lectura no se pueda ajustar a favor:** `eta_b` se fija por la pérdida del **brazo de
   CONTROL**, nunca por la del brazo de la hipótesis. Medido: subir `eta_b` de 0.03 a 0.3 **agranda ×5 la diferencia
   SELF−MUNDO** y **empeora las dos lecturas** (pérdida del control 0.0672 → 0.0886). Quien elija la tasa mirando la
   diferencia está eligiendo el resultado.
3. **La mini-prueba de C-P1 usó semillas 1–3 y está entera en el puente**, con sus predicciones fallidas incluidas
   (MP-1 y MP-3 de C1-a, MP-C1a y MP-C1b de C1-c fallaron). Este preregistro **endurece** el criterio de P1 de 0.70 a
   **0.60** y añade el control que faltaba (MOMENTO).

## 11. Coste y quién corre qué

- **Runner:** `experimentos/nivel9_probar_si_mismo/corre_probar_si_mismo.py` (con `Pool(14)`, **lo corre el
  COORDINADOR**, reglas 3 y 11). Etapas: **1/5** identidades J1–J4 (aborta si no son 100 %) → **2/5** principal, 5
  brazos × 20 semillas × 200 000 → **3/5** MOMENTO, 20 corridas con la traza de SELF-TEST de su misma semilla →
  **4/5** retención M5 (3 brazos × 6 etapas × 20 semillas × 100 000) → **5/5** generalización M6 (3 brazos × 2 reglas
  × 20 semillas × 200 000). **Coste medido por el diseñador en un proceso** (para que el coordinador sepa qué lanza):
  **19.1 s** una corrida de SELF-TEST de 200 000, **18.0 s** una de MOMENTO, **11.6 s** una de retención (T = 100 000),
  **16–68 s** una de generalización (mundo de regla, T = 200 000). Con `Pool(14)`: ≈ 2.5 min la etapa 2/5, ≈ 0.5 min la
  3/5, ≈ 5 min la 4/5 y ≈ 6 min la 5/5 → **del orden de 15 minutos de pared**, el mismo orden que `curiosidad` o
  `largo`.
- **Humo del diseñador (UN proceso, sin `Pool`, regla 3):** `corre_probar_si_mismo.py --humo` — identidades a
  T = 10 000 y **una** corrida de SELF-TEST + su MOMENTO a T = 200 000 (**2 corridas de 200 000**, por debajo del techo
  de la regla 3). Los números que salgan se informan **tal cual, sin ajustar nada**. **El humo corre en la semilla 1**,
  que el diseñador ya vio entera en la mini-prueba: así **ninguna** de las semillas 41–60 del experimento queda
  expuesta antes de correrlo.
- **Sin commits** (regla 7): el coordinador verifica identidad, integra, commitea y lanza.


## Enmienda 1 (18 sep 2026, 00:35; escrita DESPUÉS de la serie 41–60 y ANTES de la serie 61–80; coordinador)

En 41–60: P1 OK (0.263, 20/20), P2 OK (19/20, 20/20), P3 OK (20/20), **P4 NO (15/20; se exigían 16/20)**, P5 OK (20/20 × 6),
P6 OK (px0 0.80), P7 OK. Serie nueva 61–80 (`--desde 61`), mismos brazos, mismos criterios (P4 sigue en 16/20; nada se
recalibra sobre 41–60). Añadido declarado: **dE-TEST pasa de exploratorio a brazo con criterio** — P1' recuperación
dE-TEST ≤ 0.60 × V13 en mediana y pareado ≥ 14/20; P7' veneno post ≤ 4 × V13 y muertes ≤ 1.5 × V13; P4' se apaga solo
(mismos umbrales que P4) en ≥ 16/20. Se calcula con `analiza_dE.py` sobre el JSON (regla 10 de EQUIPO.md); el runner no
cambia. Si SELF-TEST repite P1–P3 y P5–P7 y P4 vuelve a caer, el vocabulario es *"cuando no se reconoce, prueba, y se
recupera antes; el impulso de probar no se apaga del todo"* (límite medido, no órgano completo). Si dE-TEST pasa P1', P4' y
P7' en las dos series, es candidato por derecho propio: *"la sorpresa del mundo en la boca"*.

**Adenda a la enmienda 1 (00:40, antes de la serie 61–80).** Al aplicar `analiza_dE.py` a 41–60, P4' tal como lo copié de P4
(Q3 ≥ 0.20) no mide el apagado en dE-TEST: su sesgo es pequeño por construcción (Q3 = 0.13) y "se apaga" (Q2/Q4 = 0.0002) sin
llegar nunca a 0.20. **P4' queda en forma relativa, la de la propuesta original de C:** Q2 ≤ 0.10, Q4 ≤ 0.10 **y** Q2 ≤ 0.35 × Q3
**y** Q4 ≤ 0.35 × Q3, en ≥ 16/20. P4 de SELF-TEST no cambia (sigue como en el runner). Resultado retroactivo en 41–60 con la
enmienda: dE-TEST P1' OK (0.143×, 20/20), P7' OK (veneno post 62.5, muertes 271.5), P4' con la forma relativa: se calcula y se
declara junto con 61–80. Nada más cambia.

## Enmienda 2 (18 sep 2026; **escrita ANTES de la serie 81–100**; creador C, encargo del coordinador)

**Estado del que parte.** Serie 41–60: SELF-TEST 2 089 contra 7 931 de V13 (**0.263 ×**, pareado 20/20), < CONST-a
19/20, < CONST-b 20/20 con razón de sesgo en Q3 **1.011** (limpio), < MOMENTO 20/20, retención 20/20 × 6, px0 G1 0.80,
P7 OK, **P4 15/20 (NO)**. **Réplica 61–80: confirma todo** — SELF-TEST 1 761 contra 7 969 (**0.221 ×**, 20/20),
< CONST-a 20/20, < CONST-b 20/20, < MOMENTO 20/20, retención 20/20 × 6, px0 G1 0.80 (V13 0.85), P7 OK, **P4 otra vez
15/20**. **dE-TEST con la enmienda 1: 41–60 0.143 × (20/20), se apaga 20/20, P7′ OK; 61–80 0.144 × (20/20), se apaga
20/20, P7′ OK** (`probar_si_mismo_s61-80_20260918_003640`), registrado como **candidato a órgano a falta de sus
baterías**. Lo que sigue es el paquete de la tercera serie.

### E2.1 Instrumento: dos perillas nuevas, las dos inertes por defecto

Construidas por anclas con `construye_probar.py` sobre `organismo_v13p.py` **y** `organismo_v13pg.py` (el del mundo de
regla, que ya llevaba `k_testE`, así que dE-TEST puede correr sus baterías sin instrumento nuevo):

```
f       = 2*b*(1-b)                                   # cota de oraculo puntual del automodelo — identidad, no perilla
f_barra <- (1-ema_auto)*f_barra + ema_auto*f          # misma constante de tiempo
s_barraL<- (1-ema_lento)*s_barraL + ema_lento*s_a     # linea base LENTA de la propia sorpresa (ema_lento = 0.0025)
sesgo   = k_test * ( max(0, s_barra - f_barra)   si resta_cota                                   # ENMIENDA 2 (a)
                   | max(0, s_barra - s_barraL)  si resta_lenta                                  # ENMIENDA 2 (a')
                   | s_barra )                        # como hasta ahora
```

**Memoria: +2 escalares** (`f_barra`, `s_barraL`). `resta_lenta` añade **una** constante (`ema_lento`, fijada en
`ema_auto/20`); `resta_cota` **no añade ninguna** (`2b(1−b)` ya está calculado).

**Campo nuevo de sólo lectura, para la prueba discriminante (c):** `t_primer_sesgo` = primer paso `t ≥ invertir_en` en
un encuentro con sesgo aplicado > 0.05, con sus contadores `enc_post_hasta_sesgo` y `mord_post_hasta_sesgo`. No entra
en ninguna decisión.

**Identidades** (`identidad_probar.py`, 6 semillas × 3 escenarios, T = 5 000): **J1 18/18** · **J2 18/18** ·
**J3 18/18** · **J4 6/6** · **J5 18/18** (`resta_cota=True` con `k_test=0` ≡ v13: la perilla es inerte) ·
**J6 18/18** (`resta_lenta=True` ídem).

**Corrección de reporte, declarada (no cambia ninguna conducta).** `sesgo_boca` pasa a acumular el sesgo **realmente
aplicado** a la boca (`_sg`, con el `s̄_a` previo, que es el causal); antes acumulaba el `s̄_a` **ya actualizado** de ese
mismo encuentro. **La conducta es idéntica bit a bit**: comprobado viejo-contra-nuevo en los **seis brazos × 3 semillas
a T = 40 000** (15/18 idénticas en TODAS las claves; las 3 que difieren lo hacen **sólo** en `sesgo_boca`). A
T = 200 000 la media por cuarto coincide hasta el cuarto decimal (0.3056 contra 0.3055 en una semilla de tres,
idéntica en las otras dos), porque el EMA es insesgado en régimen. **Por eso P4 (15/20) en 41–60 y 61–80 NO es un
artefacto del reporte**, y esos veredictos se mantienen tal como están registrados. En `identidad_probar.py`, J3 lista
`sesgo_boca` como **clave de reporte** y compara conducta, informando el máximo de la diferencia.

### E2.2 Humo de diseño, y REFUTACIÓN DE MI PROPIA PROPUESTA antes de preregistrarla

**Cuándo y qué se vio.** Tras construir las perillas, tres corridas por forma del sesgo en las **semillas 1–3, que ya
estaban expuestas** (mini-prueba de C-P1), T = 200 000, `invertir_en` = 100 000, `k_test` = 10 en las tres. **No se
miró ninguna semilla ≥ 41.** Números observados, sin ajustar nada:

| forma del sesgo | Q1 / Q2 / Q3 / Q4 (mediana) | **razón Q2/Q3** | recuperación (mediana) |
|---|---|---|---|
| `s̄_a` (SELF-TEST, la registrada) | 0.3055 / 0.0651 / **0.3130** / 0.0592 | **0.208** | **2 375** |
| `max(0, s̄_a − f̄)` (**SELF-TEST-R**) | 0.0328 / 0.0205 / **0.0484** / 0.0169 | **0.424** | 4 614 |
| `max(0, s̄_a − s̄_aL)` (**SELF-TEST-L**) | 0.0884 / 0.0211 / **0.0801** / 0.0184 | **0.263** | 3 246 |

> **Mi predicción P4′ de C7 ("Q2/Q4 ≤ 0.02 y Q3 ≥ 0.20 en ≥ 18/20") queda refutada por mi propio humo, antes de
> correr la serie.** El valor absoluto de Q2/Q4 sí baja a ≈ 0.02 — pero **porque baja TODO unas 6 ×**, no porque mejore
> el contraste: la razón Q2/Q3 **empeora** en las dos variantes (0.208 → 0.424 y → 0.263) y la recuperación **empeora**
> en las dos (2 375 → 4 614 y → 3 246).
>
> **Mecanismo, ahora claro y escribible:** el suelo y la señal **no son separables por una resta**, porque los mueve la
> misma variable. Tras la inversión la lectura `b` se va hacia 0.5, y ahí `2b(1−b)` (la cota de oráculo) es **máxima**:
> restarla se come justamente el pico de Q3. La línea base lenta hace lo mismo con retraso. *El suelo del automodelo no
> es ruido aditivo que se pueda descontar: es la incertidumbre de su propia política, y esa incertidumbre es la señal.*

### E2.3 La prueba discriminante de latencia: también refuta mi argumento

Medida con el campo nuevo, semillas 1–3, mismo mundo:

| brazo | latencia del primer sesgo > 0.05 | encuentros hasta él | bocados hasta él | recuperación |
|---|---|---|---|---|
| SELF-TEST | **839** pasos (344 / 2 106 / 839) | 70 | 7 | 2 375 |
| **dE-TEST** | **335** pasos (24 / 335 / 387) | 35 | **2** | 745 |

> **Refutado el único argumento que me quedaba a favor del automodelo.** Yo predije en C7 que el automodelo arrancaría
> **antes** por aprender de cada encuentro (27 ×) y dE-TEST más tarde por necesitar bocados. Sale al revés: **dE-TEST
> arranca en 335 pasos con DOS bocados** y el automodelo tarda 839 y necesita 7. La razón es de escala y estaba a la
> vista: al invertir, el error de ΔE salta **1.2** en un solo bocado (de +0.8 a −0.4), mientras que el error sobre la
> acción está acotado por 1 y el EMA sólo lo incorpora a razón de `ema_auto`. Y la ventaja de densidad **no se cobra**:
> el automodelo tampoco cruza el umbral con rechazos solos — necesita 7 bocados igualmente.

### E2.4 Qué propongo para la serie 81–100 (la decisión es del coordinador)

1. **Lo que falta de verdad son las baterías de dE-TEST.** El runner acepta ahora `--baterias V13,dE-TEST,...`
   (lista de brazos que pasan por retención 4/5 y generalización 5/5; por defecto la de siempre; `MOMENTO` está
   prohibido ahí porque necesita una traza de este mundo). **Recomiendo `--baterias V13,SELF-TEST,dE-TEST`** y no
   `SELF-TEST-R`: SELF-TEST tiene dos series confirmadas y es la referencia; SELF-TEST-R está refutado en humo y no
   merece gastar 240 corridas de batería.
2. **SELF-TEST-R y SELF-TEST-L van como brazos de DIAGNÓSTICO, sin criterio**, para que mi variante quede **refutada
   con 20 semillas y registrada**, no abandonada en silencio.

**Predicciones numéricas para 81–100, escritas ahora** (las de SELF-TEST-R/L predicen que mi propia variante falla):

- **Q1′ [lo que decide]** dE-TEST pasa las SEIS etapas de retención en **≥ 18/20** cada una, y G1 px0 **≥ 0.80** y
  ≥ mediana(V13) − 0.10, con `azar` en [0.35, 0.65]. **Si pasa, dE-TEST es órgano candidato con baterías**; si no,
  es un acelerador que cobra retención o generalización, y se registra como canje.
- **Q2′ [mi variante, predicha como fallo]** SELF-TEST-R: `sesgo_boca[Q2] ≤ 0.02` y `[Q4] ≤ 0.02` en ≥ 18/20 (predigo
  que **sí**), **pero** mediana de la razón Q2/Q3 **≥ 0.35** (contra 0.21 de SELF-TEST) y mediana de recuperación
  **≥ 1.5 ×** la de SELF-TEST. **Se refuta mi refutación si la razón Q2/Q3 baja de 0.21 y la recuperación no empeora**
  — y entonces el humo de 1–3 era ruido y habría que mirarlo otra vez.
- **Q3′ [latencia]** mediana de `latencia_sesgo` de **dE-TEST < la de SELF-TEST** en **≥ 14/20** pareado, y mediana de
  `mord_post_hasta_sesgo` de dE-TEST **≤ 3** contra **≥ 5** del automodelo.
- **P1–P3 no se tocan** y siguen aplicándose a SELF-TEST tal como están en §7.

### E2.5 Lectura que dejo escrita, para que la serie pueda contradecirla

Con lo medido en dos series confirmadas más este humo: **el órgano es la sorpresa del MUNDO puesta en la BOCA**
(dE-TEST: 0.143 × y 0.144 ×, se apaga solo, arranca con dos bocados). **El automodelo fue el instrumento que encontró
dónde estaba la boca, y no es el órgano**: su suelo es estructural (la cota de oráculo que él mismo mide), no se puede
descontar sin borrar la señal, y su supuesta ventaja de densidad no aparece. Lo que **sí** queda en pie del automodelo
es una **medida**: cuánto hay de sí mismo que modelar en v13 — el 13–21 % del hueco irreducible, dentro de una banda
derivada de `hambre_boca/alpha`. Eso vale gane o pierda el mecanismo, y no depende de esta serie.
