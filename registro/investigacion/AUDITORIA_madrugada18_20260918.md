# Auditoría — bloques de la madrugada del 18 (célula de creación: B-1, A-2, A-3, C-P1) — 18 sep 2026

Sólo lectura, sin editar ni correr nada salvo este informe. Igual que el día 7: preregistro + instrumento + runner +
JSON/log de `datos/` contra la prosa del registro, no al revés. Releí `registro/EQUIPO.md` (con la **regla 10 nueva**,
nacida de mi auditoría del día 7) antes de empezar. Sin hallazgos bloqueantes. Identidades: J1–J4 (`probar_si_mismo`),
I1–I3 (`hija_dispersa`, `metaplasticidad`), ETAPA 1 (`vector_unico`) — **100 % en los cuatro JSON**; ningún `humo()`
abre `Pool`. ERR-25 (`REGISTRO_etapas_1_2.md:3710-3722`) reproduce con exactitud mi verificación anterior (n_techo=0
en el examen de congelación AB, sin dato guardado para el mundo de regla) — sin hallazgo nuevo ahí.

## Hallazgos

1. **[IMPORTANTE] B-1 hija dispersa — la Enmienda 1 no es un caso de la regla 10 (no hay subconjunto de semillas),
   es una rebaja del umbral de aprobación, y quedó sin ERR numerado ni implementación en código.**
   `PREREGISTRO_hija_dispersa.md:130-138`: tras 61–80 (P1 16/20, se exigían 18/20 → R1), la enmienda define
   **P1' = ≥14/20** para 81–100, "derivado de lo visto en 61–80" (`REGISTRO_etapas_1_2.md:3753`, admitido sin
   rodeos). Esto **no** es la regla 10 (`EQUIPO.md:29-35`): ahí se restringe la POBLACIÓN a un subconjunto
   validado por una puerta fijada antes de los datos, con los umbrales ORIGINALES intactos; aquí la población es la
   misma (las 20 semillas) y lo que baja es el propio umbral de aprobación (de 90 % a 70 % de semillas), sin puerta
   de validez de por medio — es el caso que gobierna la regla 4 ("ERR numerado, criterio nuevo, semillas nuevas"),
   y no encontré un ERR asociado. **Verificado en código:** `corre_hija_dispersa.py:163`
   (`p1 = n_p1 >= (1 if HUMO else 18)`) sigue en **18**, sin tocar, en el mismo script usado para las dos series —
   el `14` de la línea 176 es el umbral de R3/R4, que **ya estaba en 14 desde el preregistro original**
   (`PREREGISTRO_hija_dispersa.md:88,93`) y no tiene nada que ver con la enmienda. Consecuencia: P1' nunca se
   implementó, y no hizo falta — 81–100 dio 19/20 y 18/20, pasando **también** el umbral original
   (`REGISTRO_etapas_1_2.md:3805`, confirmado en `hija_dispersa_s81-100_20260918_000954.json`). **Cambio
   propuesto:** asignar un ERR a la rebaja (aunque haya quedado inerte) y decidir si P1' se implementa de verdad en
   el script o se retira del preregistro ahora que es innecesaria; si se repite este patrón, una semilla nueva podría
   pasar sólo por el umbral rebajado sin que el código lo refleje.

2. **[IMPORTANTE] C-P1 — el cambio de P4' a "forma relativa" se decidió después de ver que la copia literal de P4
   fallaba en los datos ya corridos de 41–60.** Adenda a la enmienda 1 (`PREREGISTRO_probar_si_mismo.md:284-289`):
   al aplicar `analiza_dE.py` a 41–60, el criterio copiado de P4 (`Q3 ≥ 0.20`) no podía pasar nunca para dE-TEST
   porque su `sesgo_boca[Q3]` natural es 0.13 (`G_b_sesgoQ3['dE-TEST']` en ambos JSON: 0.131/0.128) — **se vio el
   número, y en respuesta se cambió la FORMA del criterio** a `Q2,Q4 ≤ 0.35×Q3` (relativo, no absoluto). El cambio
   está bien motivado (mide la misma propiedad de forma —"se apaga solo"— de manera invariante a escala, coherente
   con la intención original de P4 en `PREREGISTRO_probar_si_mismo.md:198-199`) y se ejecuta con
   `analiza_dE.py` sobre el JSON, no en línea (cumple el mecanismo procedimental de la regla 10 aunque el caso no
   sea un subconjunto de semillas) — pero sigue siendo un criterio ajustado después de ver que la versión anterior
   fallaba, y tampoco lleva ERR numerado. **Cambio propuesto:** mismo que el hallazgo 1 — número de ERR, y regla
   derivada explícita: *un criterio "copiado" de un brazo a otro con una dinámica de escala distinta se declara con
   forma relativa DESDE EL PRINCIPIO, no se ajusta al verlo fallar.*

3. **[IMPORTANTE] C-P1 — "candidato a órgano [por derecho propio]" para dE-TEST no tiene el respaldo que el propio
   preregistro exige para SELF-TEST.** `PREREGISTRO_probar_si_mismo.md:138-141` declara, por escrito y ANTES de
   correr, que M4 (retención) y M6 (generalización) se corren para V13/SELF-TEST/CONST-b y que "dE-TEST es
   exploratorio" — un hueco declarado a propósito. La Enmienda 1 (`:277-282`) promueve dE-TEST a brazo con criterio
   conductual (P1', P4', P7') y dice que si los tres pasan "es candidato por derecho propio: la sorpresa del mundo
   en la boca" — pero nunca le corre M4/M6. Por el propio estándar del bloque (P5/P6 existen exactamente para no
   declarar una aceleración que cueste retención o generalización, `:200-201`), llamar "candidato a órgano" a un
   mecanismo sin esa verificación es prematuro — no hay ninguna medida, en ningún JSON, de si dE-TEST daña
   retención o generalización. **Cambio propuesto:** antes de usar ese vocabulario en el registro, correr M4/M6
   para dE-TEST (aunque sea en una serie corta) o cambiar la frase a "candidato conductual; retención y
   generalización sin verificar".

4. **[MENOR] C-P1 — la lectura de la guarda G-b ("razón" en Q3) etiqueta MOMENTO como "inconcluso" por un
   artefacto de métrica, no por debilidad real del control.** `corre_probar_si_mismo.py:353-360` calcula
   `razon(sesgo_boca[Q3][brazo], sesgo_boca[Q3]['SELF-TEST'])` para los cuatro controles, copiando literalmente la
   tabla de lectura del bloque 6 (`PREREGISTRO_probar_si_mismo.md:209-214`). Para CONST-a/b esto mide lo que dice
   (nivel constante, comparable en Q3). Para MOMENTO **no**: el control es un desplazamiento circular de la propia
   traza de SELF-TEST (masa conservada exactamente, `G_d_masa: true` en ambos JSON) que **por diseño** saca el pico
   de Q3 y lo manda a Q4 — así que un cociente bajo en Q3 (`G_b_razon['MOMENTO']`: 0.234/0.304 en los dos JSON) es
   la firma esperada de que el control funciona, no evidencia de que recibió menos sesgo total. El chequeo correcto
   de "cantidad total" para MOMENTO ya existe y pasó limpio: G-d. P3 (SELF-TEST > MOMENTO, 20/20 pareado en las dos
   series) es sólido; la etiqueta "inconcluso" en `G_b_LECTURA['MOMENTO']` puede leerse mal. **Cambio propuesto:**
   anotar en el registro que el "inconcluso" de MOMENTO es un artefacto de la métrica de Q3 (no aplica a un control
   de desplazamiento) y que la cantidad para MOMENTO la certifica G-d, no G-b.

5. **[MENOR] A-3 vector único — el criterio A1 ("acc idéntica") es casi una tautología condicionada a A3, no una
   prueba independiente.** Por la propia álgebra del preregistro (`PREREGISTRO_vector_unico.md:8-20`: la biyección
   `(Wp,Wn)↔(W,m)`), si A3 se cumple (el tope nunca aprieta — confirmado, `A3_max_canal: 2.812 < 3` en
   `vector_unico_s101-120_20260918_003352.json`), A1 (acc idéntica) es una **consecuencia matemática obligada**, no
   un hallazgo nuevo sobre el organismo: un PASE en A1 certifica que el código implementa bien la derivación, no que
   se descubrió algo sobre el aprendizaje. No es un error — el preregistro mismo lo declara así en su §8 ("puede
   escribirse con la mitad del estado", un enunciado de equivalencia de implementación) — pero conviene no listar A1
   junto a A2–A5 como si fuera un criterio empírico más en resúmenes futuros; es un control de identidad algebraica,
   de la misma familia que los arneses de anclas del proyecto.

## Verificado sin hallazgos

**B-1 (81–100):** vocabulario correcto — `R3_rel_gt_azar` 16/20 (k=5) y 14/20 (k=4), ambos ≥14, así que se usó el
vocabulario preregistrado fuerte y no el de repliegue de R3, como exige `PREREGISTRO_hija_dispersa.md:96-99`.
**A-2 metaplasticidad:** `metaplasticidad_s41-60_20260918_000740.json` reproduce exactamente la tabla del registro
(P1 NO 7/20 pareado, C1 NO muertes B50/BASE=52/30=1.73×, `ret_no_inv` mediana idéntica 0.6667 en los tres brazos —
consistente con un efecto minoritario que no mueve la mediana, no con un bug). **C-P1, fuga de identidad (J2):**
confirmada limpia por dos vías — J2 100 % en los dos JSON, y en código (`organismo_v13p.py:103-104`) el término de
sesgo `_sg` se anula exactamente cuando `k_test=k_testE=k_auto=0` y `test_fijo`/`traza_ext` quedan en su valor por
defecto, sin otro camino que toque `Vb`. **Controles CONST-a/b:** CONST-b sí controla cantidad de forma decisiva
(`G_b_LECTURA['CONST-b']`: "limpio", razón ≥1 en las dos series — recibe igual o más sesgo que SELF-TEST durante
TODA la corrida y aun así pierde); CONST-a es un control más débil (razón 0.56–0.64, "inconcluso" por su propia
regla de lectura) pero esto no compromete P2 porque el criterio exige superar a los DOS y CONST-b ya lo decide.

## Nota sobre ERR-25

`REGISTRO_etapas_1_2.md:3710-3722` transcribe con exactitud mi verificación anterior (`AUDITORIA_dia7_20260917.md`,
sección "Verificación adicional"): n_techo=0 en los seis escenarios del examen de congelación (mundo AB), riesgo no
discutido al diseñar v13, y la regla derivada de guardar `n_techo` — que **ya se está cumpliendo** en el bloque
nuevo (`vector_unico_s101-120...json`: `A4_n_techo_cero: true`, calculado y guardado). Sin hallazgo nuevo.

## Verificación: organismo_v13 duplicado (01:10)

**(a) Diff:** sólo docstring y **dos defaults de `run()`** cambian (`experimentos/v13_dos_vias/organismo_v13.py`
línea 15 vs `organismo/organismo_v13.py`): `eta_s=0.015→0.0`, `puerta=3→None` (v13 "dos vías" queda como v11 puro).
Resto byte a byte igual (20 líneas de diff, todas en la cabecera y esa firma). **Empírico** (scratchpad, 1 proceso,
3 semillas, T=30000, todas las claves): con kwargs **por defecto**, DIFIEREN en `W`,`W_lenta`,`Wps`,`Wns` (y en
semilla 1 también `mord`,`vis`,`deaths`,`comp` — la conducta se mueve, no sólo el valor); con `eta_s=0.015,puerta=3`
explícitos, **idénticos 3/3**. Es justo lo que avisa B: conducta distinta sólo si el llamador confía en los defaults.
**(b) Grep completo** (`import organismo_v13\b`, 24 sitios en todo el repo) cruzado con el orden de `sys.path`:
**ninguno** de los archivos que importan `organismo_v13` a secas antepone `v13_dos_vias` (`identidad_v13B.py:25`,
`identidad_v13D.py:20`, `corre_allostasis.py:95,149`, `corre_probar_si_mismo.py:129`, `identidad_probar.py:25`,
`corre_rodeo.py:72`, `corre_mapa.py:49`, `bateria_v13.py:86,99`, etc. — todos con `organismo/` primero o sin
`v13_dos_vias` en su `sys.path`). Los que SÍ anteponen `v13_dos_vias` (`corre_xor.py:11`, `corre_xor_3b.py:11`,
`corre_xor_3d.py:17`, `corre_xor_3e.py:22`, `corre_N3*.py`/`mundo_social*.py` con un segundo `insert(0,…)` a mitad
de archivo, `bateria_generaliza.py:41`/`_B.py:49`/`_D.py:48`) **no importan el nombre ambiguo**: los XOR sólo usan
`organismo_v13q3`; `bateria_generaliza.py:58` usa `importlib.import_module(INSTRUMENTOS[modulo][0])`, que resuelve
a `organismo_v13g`, nunca a `'organismo_v13'` a secas (verificado leyendo la función).
**(c)** `grep -rl 88c3574cf9cf38bf datos/` → **sólo** `v13_dos_vias_20260917_160541.{json,log}` (2 archivos), la
corrida histórica que congeló v13 — su runner (`experimentos/v13_dos_vias/corre_v13.py:66,72,76`) pasa
`eta_s=eta_s, puerta=BRAZOS[brazo]` **explícitos siempre** (barre esos valores a propósito), así que no depende de
los defaults: sus números siguen siendo válidos. El sha correcto (`cc8b16b492d4d324`) aparece 70 veces en el resto
de `datos/`. Ningún otro archivo registrado cita el sha de la copia.
**(d) Veredicto: trampa latente real, sin consecuencia medida en ningún dato registrado.** El patrón (varios
runners anteponen `v13_dos_vias`) existe y es frágil — basta que alguien añada `import organismo_v13` a secas en
uno de ellos para heredar los defaults viejos en silencio (el aviso de B, 3/6 de identidad, fue en su propio humo
de `creacion_B`, un proceso sin `Pool` que por regla no escribe en `datos/`; no localicé el script exacto —no está
aún en `PUENTE_creacion.md`— pero el mecanismo es consistente con lo medido aquí). Propongo **ERR-28** con esta
etiqueta ("trampa de import, cero corridas afectadas") y dos arreglos: (i) alinear los defaults de
`experimentos/v13_dos_vias/organismo_v13.py` con el tronco o marcar su cabecera "NO IMPORTAR SIN `eta_s`/`puerta`
EXPLÍCITOS"; (ii) mover `organismo/` a la posición 0 en los `corre_xor*.py` (hoy inofensivo, pero frágil).
