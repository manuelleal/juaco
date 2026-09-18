# v14c — COMPOSICIÓN de los dos candidatos a v14 con evidencia completa (hija dispersa + puerta por código)

**Escrito ANTES de correr, 18 sep 2026.** `registro/PROPUESTA_v14.md` deja tres candidatos con evidencia completa;
dos de ellos son **componibles porque actúan en sitios distintos** del organismo:

1. **HIJA DISPERSA POR RELEVANCIA** (perilla `mask_rel`) — actúa en el **NACIMIENTO** de la hija (qué píxeles hereda
   al dividir). Validada como órgano de experimento en el mundo de historia (3T-k, dos series) y como **NO
   REGRESIÓN** en la copia del tronco (`organismo_v13D`/`organismo_v13Don`: examen v3' 8/8, G1 0.800/G2 0.834 en
   101–120, inercia total D3).
2. **PUERTA POR EVIDENCIA DEL CÓDIGO EXACTO** (perilla `puerta_pat`, forma PATC = evidencia del código ∧ ≥ 1 celda
   consolidada) — actúa en el **RUTEO** de la boca (rápida vs. lenta), nunca en el aprendizaje. Validada con examen
   v3' 8/8 en DOS series (101–120 y 121–140, 39/40 en el subcriterio E2), generalización intacta y capacidad de v11
   en el paso largo (`organismo_v13Bn5c`).

El tercer candidato de la propuesta ("la sorpresa del mundo en la boca", v13E/k_testE) **queda fuera**: cayó G1 de
generalización (0.750 < 0.80) por el preregistro de `PREREGISTRO_v13E.md` y no se declaró candidato sin dosis nueva.
No se compone aquí.

**Hipótesis:** los dos órganos no interfieren — actúan en mecanismos disjuntos (división de celdas vs. ruteo de la
boca) que no comparten estado ni se leen entre sí — y la composición conserva lo que cada uno aporta por separado.
Si el director acepta ambos, este es el preregistro que los prueba juntos ANTES de proponerlos juntos como v14.

## 1. Qué se prueba, y qué no

No es una demostración de que la composición vale MÁS que cada candidato solo (eso no se predice ni se pide);
es la prueba de que **no interfieren**: que encender los dos a la vez no rompe lo que cada uno ya tiene cerrado
(retención, generalización) y que, donde la hija dispersa sola ya mostraba ventaja (el mundo temporal 3T-k), la
composición no la borra. C4 (capacidad en el mundo grande) es exploratorio: no hay evidencia previa de qué hace la
hija dispersa ahí sola (nunca se midió), así que no hay cláusula de refutación para C4 — se mide y se reporta.

## 2. Instrumentos (por anclas; ningún original tocado)

Constructor único: `construye_v14c.py`. Aplica, en este orden, `pon_hija()` (de
`experimentos/nivel7_hija_dispersa/construye_v13D.py`, importado sin cambios) y `pon_puerta()` (de
`experimentos/nivel4_puerta_codigo/construye_puerta_codigo.py`, importado sin cambios) sobre cada origen. Las DOS
funciones parchean la misma línea de cierre de argumentos (la última línea de firma); se resuelve aplicando hija
dispersa primero y pasándole a `pon_puerta()`, como su propia ancla de firma, el texto que dejó el primer parche (no
el original) — `pon_puerta()` no cambia, solo cambian los argumentos con que se la llama. Declarado y verificado en
el propio script: cada ancla se comprueba en tiempo de construcción (aparece exactamente una vez) y aborta si no.

| archivo | origen (solo lectura) | sha origen | sha generado |
|---|---|---|---|
| `organismo_v14c.py` | `organismo/organismo_v13.py` **(CONGELADO)** | `cc8b16b492d4d324` | `649851c0f10c3cd6` |
| `organismo_v14c_on.py` (las DOS perillas fijas ON) | `organismo_v14c.py` | — | `00e941c861896455` |
| `organismo_v14gc.py` (mundo de regla) | `experimentos/v13_dos_vias/organismo_v13g.py` | `2a80e125f8593bf2` | `dcca1ab79d86289b` |
| `bateria_v14c.py` | `organismo/bateria_v13.py` **(CONGELADA)** | `1a027bcb37eb536e` | `94d035c5bfffa2e1` |
| `bateria_generaliza_v14c.py` | `organismo/bateria_generaliza.py` **(CONGELADA)** | `46772f5a582872c8` | `168a38f5adce396b` |
| `organismo_capBD.py` (mundo grande, C4) | `experimentos/nivel4_puerta_codigo/organismo_capB.py` (ya corrido) | `8070351683837077` | `e215b0148bc2c4fc` |
| `organismo_capBD_on.py` | `organismo_capBD.py` | — | `506b5c08441fd54e` |
| `mundo_composicion_v14.py` (3T-k, C3) | `experimentos/nivel7_hija_dispersa/mundo_hija_dispersa.py` (ya corrido) | `d305d53186fcbcd6` | `a9098933b1950e3d` |
| `construye_v14c.py` | — | — | `5f2f98d1ca57db79` |
| `identidad_v14c.py` | — | — | `2cea98f9ca647e90` |
| `corre_composicion_v14.py` | — | — | `647736fe3bfb2708` |

Las dos baterías son copias por anclas que **solo cambian el módulo que importan y las rutas** (viven fuera de
`organismo/`); las seis etapas, los `CRIT` importados, los umbrales del criterio v3' y los criterios G1/G2/K quedan
INTACTOS. El **criterio 5 de `bateria_v14c.py`** (identidad interna: `v13.run(seed, eta_s=0, puerta=None, ...)` debe
igualar a v11/v10) **no necesitó adaptarse** — a diferencia de v13E/ERR-30, que actuaba en la boca sin pasar por
`eta_s`/`puerta`: aquí `puerta_pat` queda **estructuralmente** sin efecto con `puerta=None` (el ternario de
`pon_puerta()` mira `puerta is None` ANTES de llamar a `_fam()`, sea cual sea `puerta_pat`), y `mask_rel=2` ya se
demostró **empíricamente inerte** en este mundo de 6 píxeles y un solo objeto (`bateria_v13D.py` corrió su propio
criterio 5 con `organismo_v13Don` — `mask_rel=2` activo — y el examen 8/8 completo solo pudo producirse si pasó: la
batería aborta si el criterio 5 falla). Sigue siendo una **predicción, no una repetición de prueba**: los dos
mecanismos juntos en el criterio 5 no se habían probado antes de esta composición. Se preregistra como **control que
puede fallar**: si falla, `bateria_v14c.py` aborta antes de la etapa 2 y C1 no es medible en esa corrida.

`organismo_capB.py` no traía la máscara de relevancia (solo `puerta_pat`) y `mundo_hija_dispersa.py` no traía la
puerta por código (solo `mask_rel`); a cada uno se le aplicó SOLO el parche que le faltaba. Diferencia real hallada y
declarada en `construye_v14c.py`: en `organismo_capB.py` la línea de traza (`P=pats[kk]; idx=...; mu[idx]=...`) vive
**fuera** de `if plast:` (4 espacios menos que en `organismo_v13.py`, donde sí está adentro); el texto de reemplazo
de `pon_hija()` para esa ancla trae la indentación escrita a mano y no calzaba ahí (`IndentationError` en el primer
intento) — se resolvió reproduciendo las cinco sustituciones de `pon_hija()` a mano para ese archivo, con la
indentación corregida (firma/estado/máscara/herencia son el mismo texto exacto).

### Identidad (obligatoria, EQUIPO.md regla 2) — **30/30**, un solo proceso, sin `Pool`

`python experimentos/nivel10_composicion_v14/identidad_v14c.py` (216.6 s):

| # | comparación | resultado |
|---|---|---|
| (a) | `organismo_v14c`(apagado) ≡ `organismo_v13` — 3 semillas × 3 escenarios, todas las claves | 9/9 |
| (b) | `organismo_v14c`(solo `mask_rel=2`) ≡ `organismo_v13Don` — 3 semillas | 3/3 |
| (c) | `organismo_v14c`(solo `puerta_pat=5,pat_min=1`) ≡ `organismo_v13Bn5c` — 3 semillas | 3/3 |
| (d) | `bateria_generaliza_v14c`(`organismo_v14c`) ≡ `bateria_generaliza`(`organismo_v13`) línea a línea, 3 semillas | 1/1 |
| (e)* | `organismo_v14gc`(apagado) ≡ `organismo_v13g` — 2 reglas × 3 semillas | 6/6 |
| (f)* | `organismo_capBD`(apagado) ≡ `organismo_capB` — 3 casos (mundo grande) | 5/5 |
| (g)* | `mundo_composicion_v14`(apagado) ≡ `mundo_temporal_k` — 3 semillas, arm C3, k=5 | 3/3 |

(\* no pedidos por nombre en el encargo; obligatorios por la regla 2 de EQUIPO.md para cualquier instrumento nuevo,
que aquí incluye los de C3/C4). (b) y (c) son más fuertes que "no rompe nada": prueban que, semilla a semilla y en
TODAS las claves del `dict` que devuelve `run()` (no solo `W`), tener la otra perilla en el código sin encenderla es
exactamente como si esa otra perilla no existiera. Es la evidencia estructural detrás de la hipótesis de "no
interferencia"; C1–C3 la prueban con las DOS perillas encendidas a la vez, que es lo que (a)-(g) no pueden probar.

## 3. Mecanismos (sin cambiar una constante de ninguno de los dos)

- **Hija dispersa** (`mask_rel=2`): al dividir, `kj = clip(KW[c]·0.95 + paso·dist, 0, 5) · rel`, con
  `rel[i] ⟺ P[i]>0 ∧ (|m̂p[i]−m̂n[i]| > δ_s ∨ min(m̂p[i],m̂n[i]) > 1−δ_c)`, `m̂p`/`m̂n` medias de `P` condicionadas al
  signo de `R` (EMA `ema_c=0.05` con normalizador). `δ_s=δ_c=0.25`. Memoria: dos vectores y dos escalares por celda.
- **Puerta por código** (`puerta_pat=5, pat_min=1` = PATC): `familiar(P) ⟺ ncod[código(P)] ≥ 5 ∧ (≥ 1 celda de su
  código con |Wp−Wn| > 0.2)`; decide qué vía consulta la boca. Memoria: un entero por código visto y su orden de
  aparición. No toca `Wp`, `Wn`, `KW` ni el aprendizaje.

Los dos puntos son los YA CONFIRMADOS: `mask_rel=2` (organismo_v13Don) y `puerta_pat=5, pat_min=1` (organismo_v13Bn5c,
la forma PATC de la enmienda 1, NO `organismo_v13Bn5` = PAT sin enmendar). No se barre nada aquí.

## 4. Diseño — `corre_composicion_v14.py`

Orquesta las cuatro medidas como **subprocesos secuenciales** (C1/C2 abren cada uno su propio `Pool(14)`, heredado
sin cambios de `bateria_v13.py`/`bateria_generaliza.py`; C3/C4 abren su `Pool(14)` directo en el proceso del
orquestador, pero solo después de que el subproceso anterior ya terminó) — un solo `Pool` vivo a la vez (regla 11).
Log desde el arranque con `fsync` (regla 10). JSON `datos/composicion_v14_<stamp>.json` con meta + shas + veredictos.

- **C1** (retención): `bateria_v14c.py 20 --desde 101 --log`, con `organismo_v14c_on` (las DOS perillas ON).
- **C2** (generalización): `bateria_generaliza_v14c.py organismo_v14c_on 20 --desde 101 --log`. **El runner
  recalcula G1/G2/K desde los números crudos por semilla (`corridas` del JSON) con los umbrales de ESTE preregistro
  (0.80/0.85), no con los que trae de fábrica `bateria_generaliza.py` (0.65/0.55)** — regla derivada de ERR-31
  (`corre_baterias_v13E.py` imprimió un veredicto que no era el del preregistro).
- **C3** (composición temporal): `mundo_composicion_v14.run(seed, arm='C3', kprof=5, T=100000, mu_norm=True,
  div_signo=True, eta_s=0.015, puerta=3, **brazo)`, brazos `V13` (las dos apagadas) y `COMP` (las dos ON), semillas
  61–80 — la MISMA serie donde ya se midió la hija dispersa sola a k=5 (sep 3.09, lift_q4 0.251, celdas 48
  medianas; `registro/REGISTRO_etapas_1_2.md`).
- **C4** (capacidad, exploratorio): `organismo_capBD.run(...)` sobre el montaje de `reverificacion_v13`
  (D=10, 60 estímulos, pasos 20 000 y 60 000, semillas 41–60), brazos `v13` (`eta_s=0.015,puerta=3`) y `COMP`
  (+ `puerta_pat=5,pat_min=1,mask_rel=2`); `N*` = mayor `n` con mediana `|W−R| ≤ 0.3` en todos los checkpoints hasta
  `n` (`mundo_grande.techo`, copia literal de `parte2_capacidad.techo`).

`--humo` (un solo proceso, sin `Pool`, sin lanzar ningún subproceso; probado, ver §7): identidad en miniatura (2
semillas) + C3 con 2 semillas y T corto + C4 con 2 semillas y mundo chico. **No mide C1/C2**: `bateria_v14c.py` y
`bateria_generaliza_v14c.py` abren `Pool(14)` sin condición (lo heredan de los originales; no tienen modo de una
sola corrida) y un implementador no corre `Pool` (regla 3 de EQUIPO.md) — C1/C2 los corre el coordinador, sin
`--humo`. `--solo C1,C2` (sin `--humo`) restringe la corrida real a esas medidas.

## 5. Predicción numérica (umbrales fijados AHORA, antes de correr nada de esto)

- **C1.** Examen v3' completo: **8/8** veredictos decisivos en `True` (`5_identidad, 1_cientificos, 2_celdas,
  3_control, 4a_identidad, 4b_sin_conflicto_no_divide, 4c_misma_valencia, 4d_causa`), semillas 101–120.
- **C2.** `organismo_v14c_on` en el mundo de regla: **G1 ≥ 0.80**, **G2 ≥ 0.85**, **K = 20/20** (cobertura ≥ 6 en
  las 20 semillas, más estricto que el `≥ 90 %` de la batería original), semillas 101–120.
- **C3.** Semillas 61–80, k=5, T=100000, con las DOS perillas ON, contra el brazo `V13` (las dos apagadas) **de la
  misma corrida**: `lift_q4` mediana **≥ 0.25** y `lift_q4`(COMP) > `lift_q4`(V13) pareado en **≥ 15/20**;
  `celdas`(COMP) ≤ 0.75 × `celdas`(V13) pareado en **≥ 14/20**. Adicional, no bloqueante: COMP debe alcanzar o
  superar la referencia YA REGISTRADA de la hija dispersa sola en esta misma serie y k (lift_q4 0.251, celdas 48
  medianas) — evidencia de que la puerta no le quita nada a la hija dispersa en el mundo donde esta sí actúa.
- **C4** (exploratorio, sin cláusula de refutación). `N*` mediana de `COMP` **≥ 48** a paso 60 000, semillas 41–60
  (referencia: v13 solo 35; PATC solo 50.5, registro `puerta_codigo_s41-60_20260918_013618`).

## 6. Cláusulas (escritas antes; nada se recalibra después de ver datos)

- **Si C1 o C2 caen** (cualquier veredicto decisivo en `False`, o G1/G2/K por debajo del umbral): **los órganos
  interfieren y NO se proponen juntos** para v14. No se reintenta con otra semilla ni se ajusta ninguna constante.
- **Si C3 cae** (no llega a `lift_q4 ≥ 0.25` y `> V13` en `≥ 15/20`, o no llega a `≤ 0.75×V13` en `≥ 14/20`): **la
  puerta anula la ganancia de composición** de la hija dispersa en el mundo donde esta se demostró — aunque C1/C2
  pasen, no se propone la combinación como reemplazo de la hija dispersa sola en ese frente.
- **C4** no tiene cláusula de refutación (§1): se mide y se reporta junto con lo demás; no decide si v14c se
  propone o no.
- Si C1–C3 pasan: lo declarable es *"la hija dispersa y la puerta por código no interfieren: cada una compone lo
  que ya componía sola, y juntas conservan retención y generalización del tronco"* — y ENTONCES, y solo entonces,
  v14c (con las dos perillas fijas ON, `organismo_v14c_on.py`) se propone al director como composición candidata a
  v14, con su propio paso de congelación (gemelo compilado, manifiesto) si lo acepta. Prohibido: "coopera",
  "se complementan", "se refuerzan" — lo que se mide es que no se dañan, no que se ayuden.

## 7. Humo — probado, ver mensaje del corredor

`python experimentos/nivel10_composicion_v14/corre_composicion_v14.py --humo`, un proceso, sin `Pool`: identidad en
miniatura + C3 (2 semillas, T=3000) + C4 (2 semillas, D=10, n_est=8, paso=500). Salida y tiempo en el mensaje final
del implementador.


## Enmienda 1 (coordinador, 18 sep 2026, 04:00; escrita DESPUÉS de la corrida 03:32 y ANTES de la réplica)

Resultado: C1 7/8 (E2 19/20, `come B Q4 ≥ 50`, la misma fragilidad de PATC solo en 101–120 que pasó 8/8 en 121–140), C2 OK
(1.000 / 0.94), C3 lift 0.237 (< 0.25; > V13 18/20; celdas 53 vs 90), C4 OK (51). Por la letra: "interfieren, no se proponen
juntos". **Réplica de C1 en semillas nuevas 121–140, misma letra (8/8)**: si pasa, la composición entra a la propuesta como opción
conjunta con C3 registrado tal cual; si E2 (u otra etapa) vuelve a caer, los candidatos se proponen por separado. C3 no se
recalibra ni se repite. Nada más cambia.
