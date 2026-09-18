# composicion_tres — COMPOSICION DE LOS TRES candidatos a v14 (hija dispersa + puerta por codigo + la sorpresa del mundo en la boca, dosis 5)

**Escrito ANTES de correr, 18 sep 2026.** `experimentos/nivel10_composicion_v14/PREREGISTRO_composicion_v14.md` midio
la composicion de DOS candidatos (hija dispersa + puerta por codigo, v14c) y la dejo sostenida en lo medido (C1-C4,
con la replica del examen en 121-140). El TERCER candidato de `registro/PROPUESTA_v14.md` ("la sorpresa del mundo
en la boca", predictor de dE del bloque 6 entrando en la BOCA, `k_testE`) quedo FUERA de esa composicion a
proposito: a dosis 10 cae la generalizacion de valor (G1 0.750 < 0.80, `PREREGISTRO_v13E.md`); a dosis 5 (bloque de
dosis, 18 sep 03:32) cumple las SEIS condiciones a la vez (recuperacion 0.267x-0.248x en dos series, se apaga
20/20, G1 0.80, G2 0.857-0.89, K 20/20, examen v3'' 8/8) y volvio a la propuesta como segundo candidato, a dosis 5
(`organismo_v13E_k5.py`). Este preregistro prueba si los TRES entran juntos.

**Hipotesis:** los tres organos actuan en mecanismos disjuntos -- hija dispersa en el NACIMIENTO de la hija
(division), puerta por codigo en el RUTEO de la boca (rapida vs. lenta), dE-TEST en el SESGO de la boca (si
prueba o no, `Vb += k_testE*s_barra_E`) -- y no comparten estado ni se leen entre si. La composicion de DOS ya
demostro que "no interferir" es medible y se sostiene (v14c). Este preregistro mide si la TERCERA pieza, que a
diferencia de las otras dos SI es un mecanismo activo (no se predice inerte: es su razon de ser acelerar la
recuperacion), sigue acelerando la recuperacion IGUAL DE BIEN cuando viaja con las otras dos, y si las otras dos
siguen intactas cuando ella viaja con ellas.

## 1. Que se prueba, y que no

No es una demostracion de que el trio vale MAS que cualquier subconjunto solo (eso no se predice ni se pide). Es
la prueba de que **no interfieren**: que encender los TRES a la vez no rompe la retencion ni la generalizacion que
la pareja (v14c) ya tiene cerradas (T1, T2), y que la sorpresa en la boca sigue recuperando rapido y apagandose
sola EN COMPAÑIA de las otras dos, con la misma vara que se le exigio sola (T3). T4 (composicion temporal 3T-k, el
frente donde la hija dispersa sola ya mostro ventaja) se deja preregistrado con su prediccion, pero se declara **NO
MEDIBLE en este paquete** (razon en la seccion 4).

## 2. Instrumentos (por anclas; ningun original tocado)

Constructor unico: `construye_v14t.py`. Aplica, sobre `organismo_v14c.py`/`organismo_v14gc.py` (que YA traen hija
dispersa + puerta por codigo apagadas), la TERCERA perilla importando los parches de `construye_selfmodel.py`
(automodelo SELF/MUNDO/H_SHUF, entrelazado, apagado) y `construye_probar.py` (predictor de dE en la boca,
`k_testE`) como DATOS -- nunca reescritos a mano -- y reproduciendo a mano (leidos linea a linea de esos dos
scripts, que no exponen una funcion `pon_X(texto)->texto` reusable) la secuencia de insercion. Declarado y
verificado en el propio script: cada ancla se comprueba por CONTEO EXACTO en tiempo de construccion y aborta si no
coincide.

| archivo | origen (solo lectura) | sha origen | sha generado |
|---|---|---|---|
| `organismo_v14t.py` | `organismo_v14c.py` | `649851c0f10c3cd6` | `fc4a803019116a88` |
| `organismo_v14t_on.py` (las TRES perillas fijas ON) | `organismo_v14t.py` | -- | `b2bcf9f5591efcfa` |
| `organismo_v14gt.py` (mundo de regla) | `organismo_v14gc.py` | `dcca1ab79d86289b` | `9ffe024e6757ac98` |
| `bateria_v14t.py` | `organismo/bateria_v13.py` **(CONGELADA)** | `1a027bcb37eb536e` | `fe5beafd90c1f4f0` |
| `bateria_generaliza_v14t.py` | `organismo/bateria_generaliza.py` **(CONGELADA)** | `46772f5a582872c8` | `e2e4c2f9ddf2a8e6` |
| `construye_v14t.py` | -- | -- | `fbc3e88ba28ae761` |
| `identidad_v14t.py` | -- | -- | `a9fb85c96a03d8c1` |

Los parches de la tercera perilla se leyeron de `experimentos/creacion_C/construye_selfmodel.py`
(`27c91df159a1465b`) y `experimentos/nivel9_probar_si_mismo/construye_probar.py` (`dd42e0170a014cbb`), ambos
instrumentos YA CORRIDOS (identidad_selfmodel.py, identidad_probar.py, identidad_v13E.py) -- solo se LEEN e
IMPORTAN como datos.

### Colision de anclas (declarada y resuelta; verificada por conteo exacto tras cada parche)

Una sola real, igual que en `construye_v14c.py`: **la firma**. `construye_probar.py` usa como ancla el ULTIMO
texto de la firma de `organismo_v13.py`/`organismo_v13g.py` (`...puerta=3):` / `...sonda_final=False):`), que ya
no existe en `organismo_v14c.py`/`organismo_v14gc.py` (la composicion de DOS ya la reemplazo por
`...puerta=3,mask_rel=0,...,pat_min=0):` / `...sonda_final=False,mask_rel=0,...,pat_min=0):`). Se resuelve
EXACTO como `compone()` de `construye_v14c.py` resolvio la suya: `pon_dE()` (en `construye_v14t.py`) recibe el
texto YA parchado por la composicion de dos como SU ancla de firma, no el original de v13/v13g.

Las otras nueve anclas de `construye_probar.py` (estado, boca, paso, predictor/dlt, bocado, las cuatro `eta ->
_eta`, `t_ext_B`, `deaths_post`, salida) se verificaron UNA A UNA leyendo `organismo_v14c.py` y
`organismo_v14gc.py` enteros antes de escribir el constructor:

- **estado** (`Wps=np.zeros(6); Wns=np.zeros(6)`) y **bocado** (`R=R_VAL[val[kk]];...;mord[kk][q(t)]+=1`) son
  puntos de insercion COMPARTIDOS con hija dispersa y puerta por codigo -- ya resueltos por `construye_v14c.py`
  (cada parche solo AGREGA texto justo tras el ancla, sin tocarla, asi que la insercion siguiente la sigue
  encontrando exactamente una vez). La tercera perilla es la TERCERA insercion sobre esas dos anclas compartidas;
  el conteo exacto se comprobo al construir (ver salida de `construye_v14t.py` en la seccion 7).
- La linea de la **boca** (`Vb=alpha*_wt+hambre_boca*hambre+.5; pb=...; mordio=...`), la de **paso**
  (`hambre=...;pat=PAT[k]`/`P_[k]`), la de **dlt** (donde se ancla el predictor de dE), las CUATRO de
  `eta -> _eta`, y las de `t_ext_B`/`deaths_post`/salida quedan BIT A BIT identicas a `organismo_v13.py`/
  `organismo_v13g.py` dentro de `organismo_v14c.py`/`organismo_v14gc.py`: ni la hija dispersa ni la puerta por
  codigo las tocan. `pon_dE()` las usa tal cual, sin adaptar nada.

### El automodelo SELF viaja entrelazado, apagado, y se declara (lo que pide el encargo)

`construye_probar.py` (ya corrido, no se edita) aplica el automodelo SELF/MUNDO/H_SHUF de
`construye_selfmodel.py` en el MISMO paso que el predictor de dE: `CS.ESTADO` se inserta en el mismo punto que el
estado nuevo del predictor, y el sesgo de la boca (`_sg`, que trae `k_testE*_sbarE`) esta escrito en la MISMA
insercion que `CS.BLOQUE` (que calcula `_sbar`, la sorpresa sobre si mismo -- solo la lee `k_test`, que aqui se
queda apagado). Separarlos exigiria reescribir `construye_probar.py` a mano, prohibido (instrumento ya corrido).
Por eso el automodelo entero viaja en `organismo_v14t.py`/`organismo_v14t_on.py`, con TODAS sus perillas en su
default APAGADO: `eta_b, k_auto, ema_auto, k_test, test_fijo, buf_auto, clip_b, eta_e, h_pred, buf_e` (el
automodelo SELF/MUNDO/H_SHUF y el automodelo a *h* pasos), mas `n_traza, traza_ext, desfase, k_testM` (control
MOMENTO) y `resta_cota, resta_lenta, ema_lento` (ENMIENDA 2 de `PREREGISTRO_probar_si_mismo.md`). **Ninguna de
estas diecisiete perillas se enciende jamas en `organismo_v14t_on.py`**; las TRES perillas propias de v14t son
solo `mask_rel` (hija dispersa), `puerta_pat`+`pat_min` (puerta por codigo, PATC) y el trio que se mueve junto
`eta_pred`+`ema_pred`+`k_testE` (dE-TEST, dosis 5).

### Identidad (obligatoria, EQUIPO.md regla 2) — **25/25**, un solo proceso, sin `Pool` (215.5 s)

`python experimentos/nivel10_composicion_v14/identidad_v14t.py`:

| # | comparacion | resultado |
|---|---|---|
| (a) | `organismo_v14t`(apagado) == `organismo_v13` — 3 semillas x 3 escenarios, todas las claves | 9/9 |
| (b) | `organismo_v14t`(`mask_rel=2, puerta_pat=5,pat_min=1`) == `organismo_v14c_on` — 3 semillas | 3/3 |
| (c) | `organismo_v14t`(`eta_pred=0.03,ema_pred=0.05,k_testE=5.0`) == `organismo_v13E_k5` — 3 semillas | 3/3 |
| (d) | `organismo_v14t_on`(`eta_s=0,puerta=None,k_testE=0,eta_pred=0`) == `organismo_v11` — 3 semillas [ERR-30] | 3/3 |
| (e)* | `organismo_v14gt`(apagado) == `organismo_v13g` — 2 reglas x 3 semillas | 6/6 |
| (f)* | `bateria_generaliza_v14t`(`organismo_v14t`) == `bateria_generaliza`(`organismo_v13`) linea a linea, 3 semillas | 1/1 |

(\* no pedidas por nombre en el encargo; obligatorias por la regla 2 de EQUIPO.md). (d) es el CRITERIO 5 que usara
`bateria_v14t.py` en T1: reduce `organismo_v14t_on` (las TRES perillas YA fijas ON) apagando SOLO `eta_s, puerta,
k_testE, eta_pred` -- `mask_rel=2` y `puerta_pat=5,pat_min=1` quedan sin apagar, y el resultado sigue siendo
`organismo_v11` bit a bit. Esto confirma, con los TRES mecanismos juntos, la misma prediccion que
`construye_v14c.py` hizo para la pareja (`puerta_pat` estructuralmente inerte con `puerta=None`; `mask_rel=2`
empiricamente inerte en este mundo de 6 px y un objeto).

## 3. Mecanismos (sin cambiar una constante de ninguno de los tres)

- **Hija dispersa** (`mask_rel=2`): al dividir, `kj = clip(KW[c]·0.95 + paso·dist, 0, 5) · rel`, con `rel` una
  mascara de relevancia por contexto (medias de `P` condicionadas al signo de `R`). Igual que en v14c.
- **Puerta por codigo** (`puerta_pat=5, pat_min=1` = PATC): `familiar(P) <=> ncod[codigo(P)] >= 5 y (>= 1 celda de
  su codigo con |Wp-Wn| > 0.2)`; decide que via consulta la boca. Igual que en v14c.
- **La sorpresa del mundo en la boca** (`eta_pred=0.03, ema_pred=0.05, k_testE=5.0`): un predictor lineal de `dE`
  (retina + codigo) que aprende con regla delta a tasa `eta_pred`; su error absoluto promediado (`s_barra_E`, EMA
  `ema_pred`) entra en la boca como `Vb += k_testE·s_barra_E`. No toca `eta`, no toca `Wp/Wn/KW`. Memoria: una
  lectura lineal (`Wpe`, `Wke`) + un escalar de estado (`s_barra_E`). El punto exacto de `organismo_v13E_k5.py`
  (`PREREGISTRO_dosis_dE.md`: cumple recuperacion <= 0.60x, se apaga, G1 >= 0.80, G2 >= 0.85, K 20/20 y examen
  v3'' 8/8 a la vez).

Los tres puntos son los YA CONFIRMADOS por separado o en pareja: `mask_rel=2` + `puerta_pat=5,pat_min=1` (v14c,
sostenida en C1-C3) y `eta_pred=0.03,ema_pred=0.05,k_testE=5.0` (dosis 5, `organismo_v13E_k5.py`). No se barre
nada aqui.

## 4. Diseno — T1-T4

- **T1** (retencion, examen v3''): `bateria_v14t.py 20 --desde 101 --log`, con `organismo_v14t_on` (las TRES
  perillas ON). Si los 8 decisivos dan `True`, se corre la **replica en semillas nuevas 121-140** con la MISMA
  letra (mismo criterio 5 adaptado por ERR-30, sin recalibrar nada). Si 101-120 no da 8/8, NO se corre la replica
  (nada que replicar: la cláusula de la seccion 6 ya decide).
- **T2** (generalizacion): `bateria_generaliza_v14t.py organismo_v14t_on 20 --desde 101 --log`. El runner
  recalcula G1/G2/K desde los numeros crudos por semilla (`corridas` del JSON) con los umbrales de ESTE
  preregistro (0.80/0.85), no con los que trae de fabrica `bateria_generaliza.py` (0.65/0.55) — regla derivada de
  ERR-31.
- **T3** (recuperacion tras la inversion, LA TERCERA PIEZA EN COMPAÑIA): `corre_probar_si_mismo.py` decide sus
  brazos (`BRAZOS`) por KWARGS sobre un MODULO FIJO (`organismo_v13p`, importado sin condicion en `tarea()` para
  los tipos `'T'`/`'M'`/`'B'`, y `organismo_v13pg` para `'G'`) — no hay forma de pedirle que use OTRO modulo por
  brazo sin editarlo, y es un instrumento YA CORRIDO (`PREREGISTRO_probar_si_mismo.md`, identidades J1-J6):
  **no se toca**. `organismo_v14t_on` no es "`organismo_v13p` con otros kwargs": tiene `mask_rel`/`puerta_pat` que
  `organismo_v13p` no tiene. Por eso T3 lo mide `corre_recuperacion_tres.py`, un runner MINIMO que reproduce
  EXACTAMENTE la medida de `corre_probar_si_mismo.py` (`t_ext_B`, `recup = T-T_INV` si `t_ext_B is None` si no
  `t_ext_B-T_INV`, mismo `T=200000,invertir_en=100000`) y el criterio **P1'/P4'** de `analiza_dE.py` (la forma
  RELATIVA preregistrada en la enmienda 1 de `PREREGISTRO_probar_si_mismo.md` para brazos que actuan en la boca,
  la misma vara que ya paso `dE-TEST` solo): brazos `V13` (`organismo_v14t`, todo apagado) y `TRES`
  (`organismo_v14t_on`, las TRES ON), semillas **161-180** (nunca antes vistas por este mecanismo: 41-100 las uso
  el bloque C-P1, 101-140 los examenes de retencion/dosis, 141-160 la replica de dosis 5).
- **T4** (composicion temporal 3T-k, exploratorio, el frente donde la hija dispersa sola ya gano): **NO MEDIBLE en
  este paquete.** `mundo_composicion_v14.py` (el instrumento de C3 de `PREREGISTRO_composicion_v14.md`) es un
  instrumento YA CORRIDO (real, no solo humo: `datos/composicion_v14_20260918_033225` y su replica) escrito en el
  estilo de `mundo_hija_dispersa.py` (espacios alrededor de operadores, `Vb = alpha * _wt + ...` en vez de
  `Vb=alpha*_wt+...`, la boca en DOS lineas en vez de una) — un estilo DISTINTO del de `organismo_v13.py`/
  `organismo_v14c.py` sobre el que se verificaron las nueve anclas de la seccion 2. `pon_dE()` (este paquete)
  depende de esas anclas EXACTAS (texto compacto sin espacios); aplicarlo sobre `mundo_composicion_v14.py` sin
  verificar cada una de nuevo, linea a linea, en ese estilo, produciria una composicion NO auditada — exactamente
  lo que la regla de anclas (EQUIPO.md regla 2) prohibe. Construir un cuarto constructor
  (`mundo_composicion_tres.py`) por anclas propias, verificadas una a una para ese estilo, es un trabajo
  independiente del tamaño de `construye_v14c.py` (que ya declaro colisiones y diferencias de indentacion propias
  para ESE archivo) y queda **fuera del alcance de esta entrega**. Se deja la prediccion escrita (abajo) por si se
  construye despues: **no se inventa ningun numero.**

`--humo` (un solo proceso, sin `Pool`, sin lanzar ningun subproceso): identidad en miniatura (2 semillas) +
`corre_recuperacion_tres.py --humo` (2 semillas, T corto) invocado como subproceso de humo (sigue siendo UN
proceso vivo a la vez: el humo de T3 termina antes de que `corre_composicion_tres.py` continue). **No mide T1/T2**:
`bateria_v14t.py` y `bateria_generaliza_v14t.py` abren `Pool(14)` sin condicion (lo heredan sin cambios de los
originales congelados; no tienen modo de "una sola corrida") y un implementador no corre `Pool` (regla 3 de
EQUIPO.md) — T1/T2 los corre el coordinador, sin `--humo`. `--solo T1,T2,T3` (sin `--humo`) restringe la corrida
real a esas medidas (T4 nunca se incluye: no es medible).

## 5. Prediccion numerica (umbrales fijados AHORA, antes de correr nada de esto)

- **T1.** Examen v3'' completo: **8/8** veredictos decisivos en `True` (`5_identidad, 1_cientificos, 2_celdas,
  3_control, 4a_identidad, 4b_sin_conflicto_no_divide, 4c_misma_valencia, 4d_causa`), semillas 101-120; **si pasa**,
  replica identica en 121-140 (tambien 8/8 esperado).
- **T2.** `organismo_v14t_on` en el mundo de regla: **G1 >= 0.80**, **G2 >= 0.85**, **K = 20/20** (cobertura >= 6
  en las 20 semillas), semillas 101-120 — la MISMA letra que T2 de v14c y que `PREREGISTRO_dosis_dE.md`.
- **T3.** Semillas 161-180, T=200000, invertir_en=100000: `TRES` (organismo_v14t_on) contra `V13`
  (organismo_v14t, apagado) de la MISMA corrida: recuperacion mediana(`TRES`) **<= 0.60x** recuperacion
  mediana(`V13`) Y pareado (`TRES` < `V13`) en **>= 14/20**; se apaga solo (P4', forma relativa de `analiza_dE.py`:
  `sesgo_boca[Q2]<=0.10, sesgo_boca[Q4]<=0.10, sesgo_boca[Q2]<=0.35*sesgo_boca[Q3], sesgo_boca[Q4]<=0.35*sesgo_boca[Q3]`)
  en **>= 16/20**. Adicional, no bloqueante: veneno_post y muertes de `TRES` dentro de lo que ya midio `dE-TEST`
  solo (veneno_post <= 4x V13, muertes <= 1.5x V13) — se reporta, no decide.
- **T4** (no medible; prediccion dejada por si se mide despues, sin cláusula de refutación porque no hay evidencia
  previa de la hija dispersa sola con la sorpresa presente a la vez — igual que C4 de v14c fue exploratorio sin
  cláusula). Semillas 61-80, k=5, T=100000, brazo `TRES` (las tres ON) contra `V13` (las tres apagadas) de la
  misma corrida: `lift_q4` mediana **>= 0.25** y `lift_q4`(TRES) > `lift_q4`(V13) pareado en **>= 15/20**; el
  mismo umbral que exigio C3 de v14c a la pareja.

## 6. Clausulas (escritas antes; nada se recalibra despues de ver datos)

- **Si T1 o T2 caen** (cualquier veredicto decisivo en `False`, o G1/G2/K por debajo del umbral, en 101-120 o en
  su replica si T1 llega a correrla): **los tres organos NO van juntos.** No se reintenta con otra semilla ni se
  ajusta ninguna constante.
- **Si T3 cae** (no llega a recuperacion <= 0.60x y pareado >= 14/20, o no llega a apagado >= 16/20): **la
  sorpresa pierde su efecto en compañia** — aunque T1/T2 pasen, la tercera pieza no se propone junto con las otras
  dos; se documenta que la composicion de DOS (v14c) sigue en pie sola.
- **T4** no tiene cláusula de refutación (no es medible; ver seccion 4): no decide si el trio se propone o no.
- Si T1-T3 pasan: lo declarable es *"la hija dispersa, la puerta por codigo y la sorpresa del mundo en la boca no
  interfieren entre si: cada una compone lo que ya componia sola o en pareja, y juntas conservan retencion,
  generalizacion y la velocidad de recuperacion tras una inversion"* — y ENTONCES, y solo entonces, el trio
  (`organismo_v14t_on.py`) se propone al director como composicion candidata a v14, con su propio paso de
  congelacion (gemelo compilado, manifiesto) si lo acepta. Prohibido: "coopera", "se complementan", "se
  refuerzan" — lo que se mide es que no se dañan, no que se ayuden.

## 7. Humo — probado, ver mensaje del implementador

`python experimentos/nivel10_composicion_v14/corre_composicion_tres.py --humo`, un proceso, sin `Pool`: identidad
en miniatura + T3 humo (`corre_recuperacion_tres.py --humo`, 2 semillas, T=3000, invertir_en=1500). T1/T2/T4 no se
miden en humo (T1/T2 exigen `Pool`; T4 no es medible). Salida y tiempo en el mensaje final del implementador.
