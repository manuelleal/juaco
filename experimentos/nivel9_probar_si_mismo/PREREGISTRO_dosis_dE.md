# dosis — ¿una ganancia menor de "la sorpresa del mundo en la boca" (dE-TEST, k_testE = 3 / 5) recupera casi tan rápido SIN pagar la generalización de valor?

**Escrito ANTES de correr, 18 sep 2026.** Sigue directamente a `PREREGISTRO_v13E.md` (examen v3'' completo,
101–120, 18 sep 02:45; entrada `registro/REGISTRO_etapas_1_2.md` "v13E — ... examen v3'' completo"): con
`k_testE = 10.0` (`organismo_v13E`, = `organismo_v13p` con `eta_pred=0.03, ema_pred=0.05, k_testE=10.0` fijos,
exactamente `BRAZOS['dE-TEST']` de `corre_probar_si_mismo.py`) "la sorpresa del mundo en la boca" **recupera 7×
más rápido** de un cambio no avisado (tres series, 41–100: 0.143×/0.144×/0.141×, pareado 20/20 × 3, se apaga sola
20/20 × 3, no envenena) y **pasa el examen v3'' de retención 8/8** en semillas 101–120, pero **la generalización de
VALOR cae por debajo de la letra**: G1 px0 **0.750 < 0.80** exigido (referencia apagada, `organismo_v13p`, en las
mismas semillas: **0.800**); G2 0.870 ≥ 0.85 sí pasa. Por el preregistro de `PREREGISTRO_v13E.md` (cláusula, §7),
**no entra al tronco tal cual**; queda como órgano de experimento con su coste anotado, y el camino declarado ahí
mismo es: *"preregistro nuevo con dosis menor (p. ej. `k_testE ∈ {3, 5}`) en semillas nuevas, exigiendo a la vez
recuperación ≤ 0.60× y G1 ≥ 0.80"*. Este documento es ese preregistro.

**Hipótesis.** El coste en G1 es una **DOSIS** de `k_testE`, no una propiedad irreductible del mecanismo: con una
ganancia menor, la recuperación sigue siendo sustancialmente más rápida que V13 (aunque menos que a `k_testE=10`)
y G1 vuelve a estar en el umbral exigido (≥ 0.80). Si es así, hay un punto en la dosis donde las dos cosas —
recuperación rápida y generalización de valor intacta— coexisten. Si **ninguna** de las dos dosis probadas aquí
logra las dos a la vez, el canje es real (§7): no es un accidente de haber fijado `k_testE=10` sin barrer.

## 1. Qué se prueba, y qué NO

Se prueban **dos dosis nuevas, preregistradas antes de verlas**: `k_testE ∈ {3, 5}` (brazos `dE3`, `dE5`). La
dosis `k_testE = 10` (brazo `dE-TEST` / `dE10` de referencia) **ya está medida** — tres series de recuperación
(41–100) y el examen v3'' completo de retención+generalización (101–120, `PREREGISTRO_v13E.md`) — y **no se
repite**: se cita como referencia, no se vuelve a correr.

**Por qué 3 y 5, no un barrido.** `k_testE=10` no se fijó por barrido sino por la mini-prueba de la célula de
creación C (`PREREGISTRO_probar_si_mismo.md`); no hay una curva dosis–respuesta medida. 5 es la mitad de 10: la
primera partición natural. 3 es aproximadamente un tercio: una dosis claramente menor, para ver si el descenso de
coste en G1 es aproximadamente proporcional a `k_testE` (en cuyo caso `k_testE=5` ya debería bastar, y `k_testE=3`
sobra en seguridad de G1 pero recupera menos) o si hay un umbral más abrupto. Dos puntos no trazan una curva
completa — no es el objetivo: el objetivo es decidir si **existe** una dosis candidata con los datos de este
bloque, no caracterizar la función dosis–respuesta entera. Si ninguna de las dos pasa, **no se prueban más dosis**
(cláusula, §7): sondear hasta encontrar una que pase sería exactamente la recalibración que la regla 3 de
`EQUIPO.md` prohíbe.

**Las cuatro trampas de la noche del 17-sep** (regla 5 de `EQUIPO.md`) no aplican de nuevo aquí: el mundo, el
mecanismo y los controles son EXACTAMENTE los de `PREREGISTRO_v13E.md`/`PREREGISTRO_probar_si_mismo.md` (mismo
mundo AB de 6 píxeles, mismo objeto, misma inversión en T/2); lo único que cambia es una constante (`k_testE`).
No se reabren esas preguntas porque nada en el mundo o el muestreo cambió.

## 2. Instrumentos (por anclas; ningún original tocado)

`construye_v13E.py` (`2491ae7dd1d91f1a`) se extendió con un argumento de dosis, **`--k K`** (`K ∈ {3, 5}`), que
genera TRES archivos nuevos por dosis (mismo patrón que el paquete v13E) y extiende `bateria_generaliza_E.py` con
las DOS dosis a la vez (para que `--k 3` y `--k 5`, corridos en cualquier orden, terminen en el mismo archivo):

| archivo | origen (sólo lectura) | sha origen | sha generado |
|---|---|---|---|
| `organismo_v13E_k3.py` | `organismo_v13p.py` | `2dbed7ccac4dd736` | `92a96be77bb66a74` |
| `organismo_v13gE_k3.py` | `organismo_v13pg.py` | `910f1f5fb64453bb` | `d8a2ac39d5425db9` |
| `bateria_v13E_k3.py` | `organismo/bateria_v13.py` **(CONGELADA)** | `1a027bcb37eb536e` | `45c25a6f707861ea` |
| `organismo_v13E_k5.py` | `organismo_v13p.py` | `2dbed7ccac4dd736` | `39574b97b0f5f56c` |
| `organismo_v13gE_k5.py` | `organismo_v13pg.py` | `910f1f5fb64453bb` | `ee10589150a950ff` |
| `bateria_v13E_k5.py` | `organismo/bateria_v13.py` **(CONGELADA)** | `1a027bcb37eb536e` | `7635ef6ff83f6e03` |
| `bateria_generaliza_E.py` (extendida, +2 entradas `organismo_v13E_k3`/`_k5` en `INSTRUMENTOS`) | `organismo/bateria_generaliza.py` **(CONGELADA)** | `46772f5a582872c8` | `c5b25e165339c569` |

La ÚNICA perilla que cambia por dosis es la constante de la firma (`k_testE=3.0` / `k_testE=5.0` en vez de
`10.0`); `eta_pred=0.03, ema_pred=0.05` quedan iguales (mismos valores medidos en `PREREGISTRO_probar_si_mismo.md`,
no se ajustan). El **criterio 5** de `bateria_v13E_k{3,5}.py` lleva el MISMO parche ERR-30 que `bateria_v13E.py`
(la reducción a v11/v10 apaga también `k_testE` y `eta_pred`, pasados EXPLÍCITOS en la llamada — no dependen de
cuál sea el default del módulo, sea 3, 5 o 10).

**Sin argumento, `construye_v13E.py` no cambió**: verificado por sha antes/después de la extensión, para los
CUATRO archivos que genera por defecto (no sólo `organismo_v13E.py`):

| archivo | sha ANTES de tocar el constructor | sha DESPUÉS (sin `--k`) |
|---|---|---|
| `organismo_v13E.py` | `ab8e3b0579edfc29` | `ab8e3b0579edfc29` — igual |
| `organismo_v13gE.py` | `882f32b4ae88b853` | `882f32b4ae88b853` — igual |
| `bateria_v13E.py` | `bed81b870faf5da5` | `bed81b870faf5da5` — igual |
| `bateria_generaliza_E.py` | `9b213f803933a9e9` | `9b213f803933a9e9` — igual (incluso corrido DESPUÉS de `--k 3`/`--k 5`: no hay dependencia de orden) |

**Identidad obligatoria** (`identidad_dosis.py`, corrida ya por el implementador, un proceso, T = 10 000; mismo
patrón que `identidad_v13E.py` partes B/C/E — la parte A, `organismo_v13p == organismo_v13`, y la parte D,
`bateria_generaliza_E.py organismo_v13p 3` línea a línea, ya están probadas ahí con el MISMO `organismo_v13p.py`
sin tocar, y no se repiten):

- **B_k** `organismo_v13E_k{K}` (defecto = dE-TEST fijo a la dosis K) == `organismo_v13p(kwargs dE-TEST,
  k_testE=K)` — 3 semillas × 3 escenarios (base, inversión en T/2, estímulo nuevo C veneno), mundo AB, mismas
  claves exactas. K ∈ {3, 5}.
- **C_k** `organismo_v13gE_k{K}` (ídem, mundo de regla) == `organismo_v13pg(kwargs dE-TEST, k_testE=K)` — 3
  semillas × 2 reglas, mismas claves exactas.
- **E_k** `organismo_v13E_k{K}(eta_s=0, puerta=None, k_testE=0, eta_pred=0)` == `organismo/organismo_v11.py` bit a
  bit en todas las claves de v11 — 3 semillas. Prueba el parche ERR-30 de CADA `bateria_v13E_k{K}.py` por
  separado (son instrumentos distintos, con su propio `import`): si esto fallara para una dosis, el criterio 5 de
  esa batería no mide nada y el examen de esa dosis no se interpreta (misma cláusula que `PREREGISTRO_v13E.md` §3).

**Resultado: IDENTIDAD 36/36 (29.6 s)** — B_3 9/9, C_3 6/6, E_3 3/3, B_5 9/9, C_5 6/6, E_5 3/3.

**Nota de implementación (--brazos).** `corre_probar_si_mismo.py` (`49ae078df2997776`) se extendió con dos brazos
nuevos en `BRAZOS` (`dE3`, `dE5`, idénticos a `dE-TEST` salvo `k_testE`) y una opción **`--brazos`** que fija QUÉ
brazos pasan por la etapa 2/5 (principal) y 3/5 (MOMENTO, si se pide): por defecto `BRAZOS_ACTIVOS` es la lista de
los ocho brazos de siempre, en el mismo orden — **sin `--brazos`, nada cambia** (verificado: `--humo`, que no pasa
por esta rama, corrió limpio después de la extensión — identidades 11/11, G-d masa `|dif| 0.0` — OK, igual que
antes de tocar el archivo). El bloque de análisis (guardas G-b/G-c/G-d, P1–P7, M5, M6, veredicto) queda **intacto,
carácter por carácter**, dentro de `if REQ_ANALISIS <= set(BRAZOS_ACTIVOS):` (verdadero siempre que corran los seis
brazos que ese bloque nombra); con `--brazos` reducido (como `V13,dE3,dE5`, sin `SELF-TEST`/`CONST-a`/`CONST-b`/
`MOMENTO`) entra por una rama nueva, más simple, que NUNCA inventa un veredicto P1–P7 con brazos que no corrieron
(los deja en `None`) y sólo reporta medianas/pareado crudos — el veredicto de la dosis lo calcula **este**
preregistro (vía `corre_dosis_dE.py`), no ese runner. La rama nueva se probó aislada (sin Pool, sin simular nada:
se extrajo el texto EXACTO del bloque con `exec` y se corrió con datos fabricados a mano, tres escenarios: 8
brazos completos, `V13,dE3,dE5` con `--baterias` a juego, y `V13,dE3,dE5` sin M5/M6) — las tres corrieron sin
excepción y con salidas coherentes. La validación de argumentos (`--brazos` con nombre desconocido, sin `V13`, con
`MOMENTO` sin `SELF-TEST`) se probó de verdad, por subprocess: las tres se rechazan antes de crear ningún `Pool`.

## 3. El mecanismo (sin cambiar una constante salvo `k_testE`)

Igual que `PREREGISTRO_v13E.md` §4:

```
b_dE  = Wpe·P + Wke·kenyon(P)                      (predictor lineal de ΔE, al morder; bloque 6, copiado)
e     = E_VAL[valencia] − b_dE  ;  s_E = |e|
Wpe  <- clip(Wpe + eta_pred·e·P,          ±clip_e)
Wke  <- clip(Wke + eta_pred·e·kenyon(P),  ±clip_e)
s̄_E  <- (1 − ema_pred)·s̄_E + ema_pred·s_E           (CAUSAL: la usa la boca del PRÓXIMO encuentro)
Vb    = alpha·w + hambre_boca·hambre + 0.5 + k_testE·s̄_E
```

`eta_pred = 0.03, ema_pred = 0.05` — los mismos de siempre, no se tocan. `k_testE ∈ {3.0, 5.0}` — las DOS dosis de
este bloque (`10.0` ya medido, referencia).

## 4. Diseño — tres medidas, subprocesos SECUENCIALES

Orquestadas por `corre_dosis_dE.py`: cada medida es un subproceso con su propio `Pool(14)`, **uno a la vez**
(regla 11 de `EQUIPO.md`).

**(a) Recuperación** — mundo largo de C-P1, semillas **121–140** (nuevas: ni 41–100, ya usadas por el brazo
`dE-TEST`/`dE10`, ni 101–120, reservadas a retención/generalización abajo):

```
corre_probar_si_mismo.py --desde 121 --brazos V13,dE3,dE5 --baterias V13,dE3,dE5
```

`V13` va SIEMPRE incluido: es la referencia dentro de la MISMA corrida (mismo patrón que P1' de C-P1 —
`recup(dosis)` contra `recup(V13)` en las MISMAS semillas, no contra el `dE10` medido en otras semillas 41–100).
`--baterias V13,dE3,dE5` añade M5/M6 (diagnóstico barato, no gate) sobre las mismas corridas. `MOMENTO` y
`SELF-TEST` no se piden: no hacen falta para esta pregunta y evitan calentar T=200 000 pasos de más por semilla.

**(b) Generalización** — semillas **101–120** (las del examen de congelación de v13, ERR-21 — las mismas de
`PREREGISTRO_v13E.md`, para comparar contra su referencia apagada ya registrada: G1 0.800 / G2 0.892,
`regresion_generaliza_organismo_v13p_20260918_*.json`, verificado en disco — **no se vuelve a correr**: es el
mismo instrumento `organismo_v13p`, sin `k_testE`, determinista en las mismas semillas):

```
bateria_generaliza_E.py organismo_v13E_k3 20 --desde 101 --log
bateria_generaliza_E.py organismo_v13E_k5 20 --desde 101 --log
```

**(c) Retención** — el examen v3'' completo (criterio 5 ADAPTADO, ERR-30, igual que `bateria_v13E.py`), semillas
**101–120** (las mismas de (b) y las del examen ya registrado de `k_testE=10`):

```
bateria_v13E_k3.py 20 --desde 101 --log
bateria_v13E_k5.py 20 --desde 101 --log
```

## 5. Análisis: umbrales propios, no prestados (ERR-31)

`corre_dosis_dE.py` calcula el veredicto de cada dosis **sobre los datos crudos** de los tres JSON (`principal` de
(a), `corridas` de (b), `veredictos` de (c)) con los umbrales de la sección 6, **fijos en el propio script**
(`UMBRAL = dict(...)`), nunca leídos del veredicto que la batería reusada imprime — es exactamente el error que
`ERR-31` nombró en `corre_baterias_v13E.py` (decidía con los umbrales de `bateria_generaliza.py`, 0.65/0.55, en
vez de los del preregistro, 0.80/0.85; el registro siguió la letra, no la impresión). El criterio 5 (retención)
**sí** se lee tal cual del JSON de `bateria_v13E_k{K}.py`: esos ocho veredictos no se piden prestados a nada, son
los umbrales originales e intactos de `organismo/bateria_v13.py`.

## 6. Predicción numérica

Una dosis es **CANDIDATA** sólo si cumple las **SEIS** condiciones **A LA VEZ** (ninguna se relaja después de ver
datos; si una sola cae, esa dosis no es candidata):

| # | condición | umbral |
|---|---|---|
| 1 | recuperación mediana / V13 mediana | ≤ 0.60× |
| 2 | pareado (recup(dosis) < recup(V13)) | ≥ 14/20 |
| 3 | apagado (P4' relativo: Q2≤0.10, Q4≤0.10, Q2≤0.35·Q3, Q4≤0.35·Q3) | ≥ 16/20 |
| 4 | G1 valor (px0 mediana, y px0>azar pareado) | ≥ 0.80, pareado ≥ 15/20 |
| 5 | G2 conducta (px0 mediana) | ≥ 0.85 |
| 6 | K cobertura | 20/20 |
| — | examen retención (criterio v3'', ocho veredictos) | 8/8 |

(El examen de retención se exige por separado, no es parte de la tabla numérica de arriba porque ya es binario
8/8 — pero SÍ es una de las condiciones que deben cumplirse a la vez para "candidata": siete condiciones en total,
contando el examen.)

**Referencia ya medida** (`k_testE=10`, `PREREGISTRO_v13E.md`, NO se repite): recuperación ≈ 0.14× (tres series,
41–100), pareado 20/20 × 3, apagado 20/20 × 3, examen 8/8, **G1 0.750 < 0.80** (falla), G2 0.870 (pasa), K 20/20.
Es la dosis que motiva este bloque: recupera de sobra, pero no candidata por G1.

**Predicción escrita para las dos dosis nuevas** (antes de correr; el mecanismo de dosis-respuesta se asume
monótono en `k_testE`, sin más base que la interpolación entre `k_testE=0` —sin coste, sin beneficio— y
`k_testE=10` —coste medido, beneficio medido—):

- **`dE5` (k_testE=5, la mitad de la referencia): CUMPLE TODO.** Recuperación ≈ 0.25× de V13 (más lenta que 0.14×
  pero de sobra bajo 0.60×), pareado ≥ 14/20, apagado ≥ 16/20 (el mecanismo ya se apaga solo a k_testE=10; a la
  mitad de ganancia no debería empeorar). **G1 ≥ 0.80**: la mitad de la ganancia cuesta aproximadamente la mitad
  del déficit (0.800 − 0.750 = 0.050 a k_testE=10 → ≈0.025 a k_testE=5, G1 ≈ 0.775–0.80; se predice que **alcanza**
  el umbral, no que lo raspa por abajo). G2 ≥ 0.85 (ya pasaba a k_testE=10 con margen, 0.870). K 20/20 (ya 20/20 a
  k_testE=10). Examen 8/8 (una dosis menor no debería romper una retención que ya cerraba con margen a la dosis
  mayor).
- **`dE3` (k_testE=3): recupera ≈ 0.40× de V13, con G1 ≈ referencia (≈ 0.80, prácticamente el mismo nivel que la
  generalización apagada, 0.800)** — es decir, casi sin coste de generalización, pero también con menos ventaja de
  recuperación que `dE5`. Pareado, apagado, G2, K y examen: se predicen iguales que `dE5` (todos ya con margen
  amplio a la dosis mayor; una dosis aún menor no los debería tumbar). Bajo esta predicción, `dE3` **también**
  sería candidata — con el perfil opuesto a `dE5` dentro del rango candidato: menos recuperación, generalización
  más intacta.

**Cláusula explícita sobre el canje (si la predicción falla).** Si **ninguna** de las dos dosis cumple las seis
condiciones a la vez — en particular si `dE5` recupera rápido pero G1 sigue por debajo de 0.80, o si `dE3` ya no
recupera lo suficiente (razón > 0.60× o pareado < 14/20) mientras G1 apenas mejora — **el canje
recuperación–generalización de valor de "la sorpresa del mundo en la boca" es real**: no es un artefacto de haber
fijado `k_testE=10` sin barrer, sino una propiedad del mecanismo (la misma señal que acelera la prueba tras un
cambio no avisado empuja un poco de prueba en lo nunca visto, y eso *es* lo que G1 penaliza). Se registra como tal
y **no se prueban más dosis** (no hay una tercera corrida "por si acaso" con otro valor de `k_testE`): eso sería
exactamente la recalibración después de ver datos que la regla 3 de `EQUIPO.md` prohíbe. El mecanismo queda fuera
de la propuesta de v14, junto a la versión `k_testE=10` ya descartada, con el coste anotado en ambas dosis.

## 7. Cláusula de refutación (escrita antes)

**Candidata** = las SIETE condiciones de §6 (las seis numéricas + el examen 8/8) TRUE a la vez, para esa dosis.

- Si **al menos una** dosis (`dE3` o `dE5`) es candidata: *"la sorpresa del mundo en la boca", a esa dosis, no
  cuesta la generalización de valor y sigue recuperando sustancialmente más rápido que V13"* — entonces, y sólo
  entonces, tiene sentido un preregistro de congelación para esa dosis (gemelo compilado con arnés de identidad,
  regla 9, y `manifiesto.py`), igual que marca `PREREGISTRO_v13E.md` §7 para el mecanismo en general. Si **las
  dos** son candidatas, la elección entre ellas (o llevar ambas) es una decisión del director, no de este bloque.
- Si **ninguna** dosis es candidata: el canje es real (§6, cláusula); se registra, no se recalibra, no se prueban
  más dosis. "La sorpresa del mundo en la boca" queda fuera de `v14` en las tres dosis probadas (3, 5, 10), con
  el coste de cada una anotado en el registro.

Nada de esto se decide DESPUÉS de leer los JSON de las tres medidas; esta sección fija el criterio ANTES de verlos.


## Enmienda 1 (coordinador, 18 sep 2026, 03:45; escrita DESPUÉS del bloque de dosis y ANTES de la réplica)

Resultado: dE5 cumple las seis condiciones (recuperación 0.267×, 20/20; apagado 20/20; G1 0.80, 17/20; G2 0.857; K 20/20; examen
8/8); dE3 no (G2 0.842; examen 7/8). **Réplica de la recuperación a dosis 5 en semillas nuevas 141–160**, mismo runner
(`corre_probar_si_mismo.py --desde 141 --brazos V13,dE5 --baterias V13,dE5`), **mismos criterios** (recuperación ≤ 0.60× V13 en
mediana y pareado ≥ 14/20; apagado P4' ≥ 16/20; retención de las seis etapas ≥ 18/20; px0 G1 ≥ 0.80). Si replica, dE5 queda con dos
series a su dosis (más tres a dosis 10); si no replica, se registra y el candidato vuelve a "pendiente". Nada se recalibra.
