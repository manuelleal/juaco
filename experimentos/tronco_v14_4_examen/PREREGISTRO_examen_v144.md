# PREREGISTRO — examen del CRITERIO DE TRONCO v4 sobre v14.4 = v14.3 + TERMO (termostato de boca)

**Escrito ANTES del humo del runner** (28-sep-2026, creador del examen). Antes de escribir esto sólo se corrió:
- la construcción por anclas (`construye_v144.py`);
- la búsqueda de semillas (`busca_semillas_v144.py`, no simula);
- el cálculo de potencia de T-G sobre datos **que ya existían** (`analiza_potencia_v144.py`, no simula);
- el arnés de identidad (`identidad_v144ex.py`), **126/126**. Imprime lecturas de una semilla de identidad (47045, T = 20 000 y un E2 de
  100 000). La sec. 5 (predicciones) se escribió **sin leer esas líneas**: sale del mecanismo y de los números del tronco en el examen
  de v14.3. La sec. 12 (humo) se escribe después y se dice.

Decisión del director (28-sep ~11:00, commit `f912697`): examen v4 de TERMO, candidato a v14.4; salvaguardas: preregistro, semillas
nuevas, serie + réplica. Encargo del coordinador: **misma letra y umbrales que el examen de v14.3, sin cambiarlos**; lo que no traslade,
como ERR candidato. Misión: llegar a la AGI por este camino. **El examen v4 es la puerta de NO REGRESIÓN del organismo común.**

## 1. Hipótesis
**H-v144:** el tronco v14.3 con la pieza TERMO no hace nada peor que v14.3 en lo que el tronco ya hace (T-A…T-F, en los mundos de la
letra) y **sube el crecimiento neto del linaje** en el mundo vivo (T-G), con el control TERMOINV que no lo hace, en semillas nuevas,
en serie y réplica.

## 2. Mecanismo, memoria y constantes (y lo que NO traslada)
- **La pieza (letra de `V143_TERMO._tm_boca`, carrera, `experimentos/organelos/termo/`).** Sobre un estímulo k que el organismo ya
  mordió, con s = media del dS **sentido** al morderlo: si s no tiene componentes negativas y tiene alguna positiva, **muerde ⇔ ∃ j:
  s_j > 0 ∧ nivel_j < U + s_j/2**. Lo desconocido y lo sentido malo (o nulo) quedan como en v14.3. La decisión se toma **después** del
  sorteo de la boca, que se consume igual: el rng no se toca.
- **Traslado:** una función de módulo sin estado, `termo_letra(m, lev, U, mf, modo)`, con el **mismo texto** en `organismo_v144`,
  `organismo_v144g` y `organismo_v144cal`. El arnés (L) la compara con `Carro._tm_boca` de los dos carros de la carrera en 18 980
  casos sintéticos: misma decisión y mismos contadores.
- **Perilla `termo`:** 0 = v14.3 bit a bit · 1 = TERMO (defecto del candidato) · 2 = TERMOINV (control de T-G; sólo con dos
  necesidades).
- **Memoria nueva: SÍ (declarado, no es cero).** En el carro, s sale de `_adS` de APR, que ya estaba. **El tronco v14.3 no tiene APR:**
  aquí `_adS` es memoria nueva. Por estímulo mordido guarda la suma del dS nominal por necesidad y el número de mordidas (2 números con
  una necesidad, 3 con dos). Se acumula como `APR._apr_dS`: **suma sin olvido**. El arnés lo comprueba contra la suma secuencial.
- **Constantes:** la consigna U = `rep_umbral` y el ½ de la pieza (del exploratorio de la carrera, declarado en `PREREGISTRO_termo.md`).
  - Mundo vivo: U = el kwarg `rep_umbral`, 1.0. En T-A lo pasa el montaje. En T-C (ii) y T-D es el defecto del organismo (1.0).
  - Mundos de una necesidad (examen v3′, mundo de regla): no hay parto. Se agrega el kwarg `rep_umbral=1.0` (el valor de la pista y
    del mundo vivo; no se ajusta) y j recorre la única necesidad (E).
- **Dónde actúa:** en todos los mundos del examen. A diferencia de N en v14.3, **no es inerte por construcción en ninguno**. Por eso
  aquí no hay "inercia"; el runner reporta cuántas corridas del candidato salen idénticas al tronco, como lectura.

## 3. Instrumento y anclas (todo en `experimentos/tronco_v14_4_examen/`; los orígenes sólo se leyeron)
| archivo | sha16 | origen (sha) | qué es |
|---|---|---|---|
| `organismo_v144.py` | `e3768f6eab05b964` | `organismo/organismo_v143.py` (`2cebc0ab0c38b70f`, CONGELADO) | el candidato (a CONGELADOS si pasa) |
| `organismo_v144g.py` | `1ea7fb43f41a69c5` | `organismo/organismo_v143g.py` (`c20fccaa9107fb89`) | su mundo de regla (a CONGELADOS) |
| `bateria_v144.py` | `e928b202d9d66702` | `organismo/bateria_v143.py` (`9daa88a90a2fd7b1`) | examen v3′ apuntando a v144 (a CONGELADOS) |
| `bateria_generaliza_v144.py` | `3263ab8d8f45e7cd` | `organismo/bateria_generaliza_v143.py` (`a894101fd1e6db93`) | + entrada `organismo_v144`, campo a campo |
| `organismo_v144cal.py` | `a5a891e1d819e1bb` | `tronco_v14_3_examen/organismo_v143cal.py` (`1169f54ef0a19de1`) | v14.4 en el mundo vivo (instrumento) |

- `construye_v144.py` (`91b7d110780f336e`) los genera por anclas (cada ancla exacta una vez). Antes comprueba que la letra está
  literal en `carros/V143_TERMO.py` (`3db639cab75641fb`). `--verifica` compara el disco con la construcción.
- En `bateria_v144`, la identidad interna contra v11/v10 (`tarea_id`) pasa `termo=0` junto a las perillas que ya apagaba. Sin eso, la
  regla 1 compararía TERMO encendido contra v11. Etapas, CRIT y umbrales: intactos.
- **El tronco contra el que se mide es v14.3:**
  - examen v3′ y T-B: `organismo/bateria_v143.py` y `organismo/bateria_generaliza_v143.py`, CONGELADAS;
  - mundo vivo: OFF, TRONCO_B y PLACEBO son las tareas calibradas de V4-CAL (`organismo_v3cal`, v14.2). En el mundo vivo **eso es
    v14.3 bit a bit** (masa 3): arnés (A′) 5/5 y examen de v14.3, 480/480 corridas.
- Reuso por import, con sha fijado en `corre_examen_v144.ANCLAS` (27 anclas): la letra calibrada `criterio_v4/corre_criterio_v4` y
  `umbrales_v4`; `corre_dE5_v2`; `corre_codigo`; `corre_sal`; `mini_vivo`; `corre_vivo_rep2`; `diagnostico_codigos`;
  `umbrales_examen_v143` (`c3becf65e9bfd8ec`: **la letra del examen de v14.3, importada**); los dos carros de TERMO; y los veredictos
  y crudos del examen de v14.3 (el arnés (J) los reproduce).
- Umbrales, semillas y predicciones: `umbrales_examen_v144.py`.
- **Arnés `identidad_v144ex.py`: RESULTADO 126/126** (144 s): (0) 6/6 · (A) 21/21 · (A′) 5/5 · (P) 10/10 · (L) 5/5 · (X) 2/2 ·
  (D) 7/7 · (R) 41/41 · (J) 10/10 · (K) 19/19. Salida en `identidad_v144ex_salida.txt`; JSON
  `datos/humo/identidad_v144ex_20260928_123012.json` (`e181554fab26fa19`).

## 4. La letra de CRITERIO_TRONCO_v4, puerta por puerta (la del examen de v14.3, sin tocar un número)
| puerta | medida y montaje | letra (umbral) | n y semillas (serie / réplica) |
|---|---|---|---|
| **T-A** | `corre_vivo_rep2` VIVO y CUELLO_MIN, T = 100 000; OFF, **CAND**, TRONCO_B (s + 100 000), PLACEBO (+ CTRL para T-G) | muertes ≤ 1.10 ×; `r` ≥ tronco − 10; NI una cola 95 % `LI > −10` | 80 / brazo: 47101–47180 / 47201–47280 |
| **T-B** | `bateria_generaliza` px0 y azar, T = 200 000, CAND (v144) y TRONCO (v143) en las mismas semillas, desde los valores crudos | G1 ≥ 0.80, G2 ≥ 0.85, azar G1 ∈ [0.35, 0.65], **azar G2 ∈ [0.31, 0.60] (ERR-122)**; la banda vieja [0.42, 0.58] se reporta y no decide; K 20/20 | 20: 47001–47020 / 47021–47040 |
| **T-C** | (i) examen E2; (ii) `mini_vivo` VIVO, `invertir_vivo_en = 50 000`, cuatro brazos; `vis[B]`, `vis[A]` al lado | (i) come B Q4 ≥ 50 en ≥ 18/20; (ii) NI `LI > −12.5` | (i) 20 como T-B; (ii) 80 como T-A |
| **T-D** | sal muda (`corre_sal.BASE`), OFF y CAND | C1, C2, C6 importados de `creacion_B/corre_codigo.UMBRALES` | 9 ALIAS + 9 LIMPIAS, las primeras de 47501–48000 / 48001–48500 |
| **T-E** | examen v3′, seis etapas, CAND contra TRONCO v14.3 en las mismas semillas | ≥ 18/20 por escenario, tolerancias 1.10 / 0.8 | 20 como T-B |
| **T-F** | celdas, divisiones, muertes | ≤ 1.25 × tronco (medianas), examen y mundo vivo (T-A y T-C ii) | los de T-A, T-C y el examen |
| **T-G** | ver abajo | ver abajo | los de T-A (+ 80 CTRL por brazo) |
| **T-H** | ESCALA | **reportada, no eliminatoria** | **NO SE MIDE** (instrumento no construido; como en v14.3) |

**T-G, la capacidad que declara el candidato.** "TERMO sube el crecimiento neto del linaje en el mundo vivo". Es lo más cercano, en los
mundos del examen, a lo que TERMO hizo en la pista (R0 real de nacimientos). La medida `r = descendientes − muertes` es la cantidad
que cuenta H-1.
- **Brazo que decide: CUELLO_MIN.** Es la regla del cerebro de la pista (FABRICA = REL de f9c = CUELLO_MIN + …), donde se midió TERMO.
  Se eligió antes de ver ningún número. VIVO se reporta y no decide.
- **G-1**, el candidato gana: `LI_95(r_CAND − r_OFF) > m`, con m = 1, z = 1.645 y n = 80, pareado nominal por semilla.
- **G-2**, el control no gana: `LI_95(r_CTRL − r_OFF) ≤ m`. CTRL = TERMOINV (`termo = 2`): la misma regla leyendo la necesidad que el
  estímulo **no** sube; misma lectura, consigna, estímulos y pasos. **Puede fallar**: si bastara comer menos o con otro ritmo,
  TERMOINV también ganaría.
- **G-3**, la pieza actúa (`a_no + a_si > 0`) en ≥ 95 % de las corridas del candidato en CUELLO_MIN.
- **Nulo, margen y n** (regla 15; `analiza_potencia_v144.py`, sobre las 160 semillas reales por brazo del examen de v14.3: OFF,
  TRONCO_B y PLACEBO; JSON `datos/humo/potencia_examen_v144_20260928_121917.json`, `4e4df40a5c3cc67d`):
  - Con m = 0, el nulo **no centrado** pasa G-1 **0.107**. La media muestral de d = TRONCO_B − OFF en CUELLO_MIN es +0.89, que es
    ruido. Eso incumple la regla 15. **Por eso m = 1**, el menor entero con el nulo ≤ 0.05.
  - Con m = 1: P(G-1 | nulo) **0.044**, P(G-2 | nulo) 0.994, **P(T-G | nulo) 0.042**. Nulo centrado: 0.016.
  - Margen: potencia de G-1 **0.883 en δ = +6** de `r` (0.76 en +5); **P(T-G) en δ = +6 con el control nulo: 0.877**.
  - n = 80 cumple ≥ 0.95 bajo el nulo y ≥ 0.80 en el margen. sd(d) medida 18.8 (CUELLO_MIN) y 16.5 (VIVO).
- **Por qué T-G es eliminatoria:** v14.4 declara una capacidad. Si esa capacidad no se ve en el organismo, en semillas nuevas, no hay
  razón para tocar el tronco. Además no es una reparación inerte: actúa en todos los mundos.

**4′ de la letra:** TRONCO_B y PLACEBO van en T-A y T-C (ii). Si TRONCO_B no pasa, la serie no se lee: se corre la RESERVA 47301–47380
(`--reserva --sustituye serie|replica`), que sustituye sólo lo del mundo vivo (T-A, T-C ii, T-F vivo y T-G). Si la reserva tampoco
se lee, el examen queda NO SE LEE y decide el coordinador con ERR.

## 5. Predicciones firmadas (p = probabilidad de que la puerta PASE en UNA serie; `umbrales_examen_v144.PRED`)
**El mecanismo que las ordena, visto antes de correr.** La memoria de lo sentido **suma sin olvido**. En un mundo que se invierte (E2 del
examen, T-C ii del mundo vivo), lo que fue bueno sigue "sentido bueno" mientras la suma sea positiva. La media sólo cambia de signo
cuando las mordidas nuevas (−0.4) pasan del doble de las viejas (+0.8).
- En el mundo vivo el tronco muerde A unas 200 veces por cuarto antes de invertir (examen de v14.3, T-C ii OFF: 206/210). Hacen falta
  del orden de 800 mordidas envenenadas para que TERMO deje de gobernar A.
- En el examen v3′ (E1: A 79 por cuarto) hacen falta del orden de 300–400.
- Mientras tanto TERMO **muerde A siempre que E < 1.4**. Es decir: **no se desdice**. La pieza de la pista nunca vio una reversión.

| puerta | predicción numérica | p |
|---|---|---|
| legible | TRONCO_B pasa T-A, T-C (ii) y T-F vivo (las mismas tareas calibradas que en v14.3) | 0.97 |
| T-A | `r` VIVO CAND mediana en [−85, −55] (OFF ≈ −72); CUELLO_MIN en [−20, +10] (OFF ≈ −7); muertes 0.85–1.15 × | 0.55 |
| T-B | G1 ≥ 0.90; G2 0.93–1.00; azar G2 0.33–0.55; K 20/20. La conducta de primer encuentro (`ba`) no la toca la pieza (lo nuevo es desconocido) | 0.90 |
| **T-C** | (i) come B Q4 ≥ 50 en ≥ 18/20 (p 0.85); **(ii) `rev` CAND mediana en [−30, +25] (OFF ≈ 42): LI > −12.5 con p 0.25** | **0.20** |
| T-D | C1, C2, C6 como el tronco: la pieza no gobierna B ni D (la sal muda tiene s nula) | 0.85 |
| **T-E** | **cae E2 "muerde A Q4 ≤ 1.10 × tronco": muerde A en Q4 (mediana) 60–250 contra ~10 del tronco** | **0.05** |
| T-F | examen p 0.80; vivo p 0.50: las muertes de T-C (ii) suben 1.1–1.6 × por las mordidas de A envenenada | 0.40 |
| **T-G** | G-1 p 0.25: d mediana en [−10, +10], sin razón fuerte de signo (en el mundo vivo no hay otros linajes que aprovechen la comida que la consigna deja); G-2 p 0.95; TERMOINV `r` ≤ OFF − 10 con p 0.7 | **0.25** |
| **serie** | producto < 0.01 | **0.005** |
| **serie + réplica** | **veredicto: NO PASA** | **PASA ≈ 0.00** |

**Mi predicción del veredicto por la letra: NO PASA (p ≈ 0.99)**. Las caídas más probables:
- T-E por E2, casi seguro;
- T-C (ii);
- probablemente T-G;
- posiblemente T-F vivo.

Si T-E y T-C caen por la reversión, **no es un defecto de la letra**: es exactamente lo que la puerta "se desdice" quiere ver.

## 6. Qué significa cada veredicto y qué refuta H
- **PASA** (serie y réplica legibles, siete puertas): v14.4 puede entrar al tronco. **Decide el director**, con el procedimiento de la sec. 10.
- **NO PASA:** no se congela; v14.3 sigue siendo el tronco. Se lee **dónde** cae:
  - (a) T-E/T-C por la reversión → TERMO **no se desdice**; es la memoria sin olvido. Refuta la parte de no regresión de H. El siguiente
    candidato (TERMO′ con memoria que olvida o se reinicia al sorprender) sería **otro** preregistro, no un ajuste de éste.
  - (b) T-G → el termostato no sube el crecimiento en el mundo vivo. Su efecto en la pista sería del sistema (varios linajes, comida
    compartida) o de su base (FILTRO + APR), no de la pieza sobre el tronco.
  - (c) T-A/T-B/T-D/T-F sin reversión → regresión directa de la pieza.
- **NO SE LEE:** TRONCO_B cae también en la reserva → ERR; no hay veredicto.
- Vocabulario si PASA: *"el termostato de boca sobre lo sentido bueno sube el crecimiento neto del linaje en el mundo vivo sin empeorar
  nada de lo que hacía v14.3, replicado"*. Prohibido: "cruza H-1", "regula como un animal", "tiene hambre".

## 7. Lo que no traslada y los riesgos de la letra vistos antes de correr (candidatos a ERR; nada se cambió por ellos)
1. **Memoria nueva** (sec. 2). "Cero memoria nueva" de TERMO era relativo al carro V143, que ya tenía APR. En el tronco, `_adS` es memoria
   nueva y sin olvido.
2. **Base distinta.** Toda la evidencia de TERMO (MODESTO ×2) es sobre el carro V143 = FABRICA + B-5 + FILTRO + APR; no sobre v14.3.
   - v14.3 + TERMO sin FILTRO ni APR **no se midió nunca en la pista**.
   - El examen mide el organismo en los mundos del tronco; la pista de la carrera no es un mundo del tronco (no hay carro del tronco).
3. **La consigna en mundos sin parto** (sec. 2): U = 1.0 como constante del organismo donde no hay reproducción.
4. **El examen no ve 3T-k.** La composición que v14.3 trajo (K_max 8) vive en `mundo_n7`, con su propio organismo. TERMO no se portó
   ahí: **no se verifica que v14.4 conserve la composición.** Recomendación: si PASA, correr 3T-k con la pieza, portada por anclas,
   antes de congelar.
5. **Margen de superioridad de T-G, m = 1** (sec. 4): sale del nulo real, no del candidato; con m = 0 la puerta incumplía la regla 15.
6. **La cláusula "come A Q4 ≥ 0.8 × tronco"** (E1, E2L de T-E) castiga comer menos. Comer menos cuando se está lleno es el mecanismo
   de TERMO. En el examen v3′ el tronco pasa hambre (130 muertes por corrida en E1 en el examen de v14.3), así que E casi nunca llega a
   1.4 y no debería pesar. Se declara por si cae ahí.
7. **La T-G decide en CUELLO_MIN y no en VIVO** (sec. 4). Si G-1 pasara sólo en VIVO, T-G cae igual. Así está escrito.

## 8. Semillas NUEVAS (`busca_semillas_v144.py`, 28-sep-2026; salida en `busca_semillas_v144_salida.txt`)
| papel | serie | réplica |
|---|---|---|
| examen v3′ y T-B | 47001–47020 | 47021–47040 |
| mundo vivo T-A (+ CTRL de T-G) y T-C (ii) | 47101–47180 (TRONCO_B 147101–147180) | 47201–47280 (TRONCO_B 147201–147280) |
| T-D ALIAS (primeras 9 con \|code(D)∩code(B)\| = 3) | 47518 47575 47597 47608 47621 47686 47713 47714 47725 | 48011 48031 48070 48071 48074 48094 48101 48116 48117 |
| T-D LIMPIAS (primeras 9 con \|D∩B\| = 0) | 47501 47508 47516 47521 47530 47554 47556 47559 47568 | 48009 48012 48017 48020 48028 48029 48030 48043 48051 |
| reserva del mundo vivo (sólo si TRONCO_B no pasa) | 47301–47380 (TRONCO_B 147301–147380) | |
| humo / identidad | 47041–47043 (+ la ALIAS histórica 326) / 47045–47047 (47044 sin uso) | |

- La búsqueda recorrió 43 957 archivos de texto de `PROYECTOS/JUACO` (repo, worktrees, sandbox, anclado, respaldo).
- En 47000–48600 y 147000–148600 sólo aparecen fragmentos de sha (`f47383fd…`, `668f16b48345…`, `e1eb48547b…`, `148014f68cb…`) y un
  número de issue (#47101).
- **Ninguno** aparece en contexto de semilla ni en nombres de archivo.
- La selección de T-D es estructural (`diagnostico_codigos.solapamientos`, sin simular); el runner la recalcula y se para si no coincide.
- Ninguna semilla coincide con V4-CAL, subida_n7, tronco_v14_3, el examen de v14.3 (43000–44600) ni TERMO (39001–39140, 39901–39914).
  Lo comprueba la regla 14 (R6).

## 9. Las cuatro trampas
1. **Canal simétrico:** no hay canal; en T-G el control es TERMOINV (misma lectura, necesidad equivocada).
2. **Acierto sin balancear:** G1/G2 de T-B son balanceados; T-G se mide en `r` (nacimientos − muertes), no en aciertos.
3. **El mundo que se come la comida:** es **parte del mecanismo** (la consigna deja comida en el mundo). Se reportan:
   - `vis[A]`, `vis[B]` por cuarto al lado de `rev`;
   - muertes por necesidad;
   - descendientes;
   - la telemetría de la pieza (decisiones gobernadas, `a_no`, `a_si`).
4. **Sitios fijos:** el mundo vivo repone en posiciones sorteadas; celdas y divisiones en T-F.

## 10. Procedimiento de congelado si el examen PASA (ESCRITO, no ejecutado; lo decide el director)
1. `python manifiesto.py --check` → 24 intactos. `python experimentos/tronco_v14_4_examen/construye_v144.py --verifica` → todo igual.
2. **Antes de congelar:** cerrar el riesgo 7.4 (3T-k con la pieza). Si v14.4 pierde la composición de v14.3, no se congela.
3. Copiar **byte a byte** a `organismo/` y comprobar sus sha:
   - `organismo_v144.py` (`e3768f6eab05b964`);
   - `organismo_v144g.py` (`1ea7fb43f41a69c5`);
   - `bateria_v144.py` (`e928b202d9d66702`);
   - `bateria_generaliza_v144.py` (`3263ab8d8f45e7cd`).

   `organismo_v144cal.py` no entra al tronco: es el instrumento del examen.
4. El bloque de `CONGELADOS` lo pega el director a mano (`JUACO_CONGELAR=1`), como en v14.3 → 28 intactos.
5. **Regla 1 nueva:** `cd organismo && python bateria_v144.py 6 && python bateria_generaliza_v144.py organismo_v144 20 --desde 101`.
   Corre con `--log`, la corre el coordinador y debe salir todo PASA.
6. `CLAUDE.md`, `ESTADO.md`, REGISTRO, commit, tag `v14.4-tronco`. Si algo de 1–5 falla, no se congela y se registra con ERR.

## 11. Comandos y costo (sólo el coordinador; los agentes no corren `--serie`, ERR-115)
Antes de cada serie el runner corre el arnés (se para si no da 126/126), la regla 14 (41/41) y la selección de T-D.
- **PC, Pool 6:** `python experimentos/tronco_v14_4_examen/corre_examen_v144.py --serie --pool 6`
- Réplica: `python experimentos/tronco_v14_4_examen/corre_examen_v144.py --replica --pool 6 --con experimentos/tronco_v14_4_examen/datos/examen_v144_serie_<sello>.json`
- Bloque (no corre nada): `python experimentos/tronco_v14_4_examen/corre_examen_v144.py --bloque <serie.json> <replica.json> [<reserva.json>]`
- Sólo si una serie no se lee: `... --reserva --sustituye serie|replica --pool 6`.
- Si el análisis se cae después de las corridas: `... --analiza experimentos/tronco_v14_4_examen/datos/examen_v144_<modo>_<sello>`.
- Nube (Pool 3): los mismos con `/root/venv-juaco/bin/python` y `--pool 3`.
- **Costo por serie: 1 476 corridas** (T-B 80 de T = 200 000; examen 240; T-D 36; T-C ii 320; T-A 800 con el CTRL de T-G). La
  duración, medida en el humo, está en la sec. 12.

## 12. Arnés y humo (UN proceso) — escrito DESPUÉS de sec. 1–11 (28-sep ~12:35). Nada de esto cambió una predicción ni un umbral
**Arnés `identidad_v144ex.py` → RESULTADO 126/126** (144 s; `identidad_v144ex_salida.txt`; JSON
`datos/humo/identidad_v144ex_20260928_123012.json`, `e181554fab26fa19`):
- (0) 6/6 · (A) 21/21 · (A′) 5/5 · (P) 10/10 · (L) 5/5 · (X) 2/2 · (D) 7/7 · (R) 41/41 · (J) 10/10 · (K) 19/19.
- Primera corrida limpia. Antes de correrlo cambié un control de (K), por construcción y sin ver datos: "gana +1 exacto" pasó a "+0.9",
  porque la resta en coma flotante no garantiza LI = 1 exacto.
- Lecturas de una semilla (identidad 47045), **no son dato**:
  - la pieza gobierna 117–1 121 decisiones por corrida y cambia la de la boca (`a_no` 56–404; `a_si` 0–30);
  - en E2 (T = 100 000) el candidato muerde A por cuarto [80, 42, 145, **102**]; v14.3, [95, 75, 35, **4**].

**Humo `corre_examen_v144.py --humo`** (15 s; 6 corridas, 200 000 pasos; JSON `datos/humo/examen_v144_humo_20260928_123241.json`,
`4650612c26e30c70`; salida en `humo_salida.txt`). **No es dato:**

| corrida | resultado |
|---|---|
| T-A CUELLO_MIN s47041, T = 20 000 | OFF `r` −7 (muertes 20) · **CAND `r` +11** (muertes 8; 423 decisiones gobernadas, `a_no` 219, `a_si` 14) · CTRL `r` −7 (muertes 17) |
| T-C (ii) CAND s47042, T = 20 000 (invierte en 10 000) | rev 1; al final A sigue "sentida buena" (suma +20.4 en 87 mordidas): el mecanismo de la sec. 5 |
| T-D CAND ALIAS 326 | \|W[sal]\| 0.01, W[veneno] −2.92 (B-5 actuando) |
| examen E2 CAND s47043 | come B Q4 183 (≥ 50); muerde A por cuarto [80, 92, 208, **128**] |

- Cableado de la etapa 8 con crudos sintéticos: el candidato bueno pasa las siete; el MALO cae T-A, T-B, T-C, T-D y T-G. Regla 14 41/41.
- `--analiza` y `--bloque` se probaron con crudos sintéticos **fuera del repo** (scratchpad), incluida la reserva que sustituye un mundo
  vivo no legible.

**Duración** (un proceso, medida en el humo): mundo vivo 6.6 s, T-C (ii) 7.7 s, sal 8.0 s y examen 6.7 s por corrida de T = 100 000; T-B
supuesto en 13 s.
- Por serie: **3.0 h de CPU**, que con **Pool 6** son **≈ 30 min** con el PC libre (el examen de v14.3 predijo 2.8 h y tardó 30 min) y
  **35–50 min** con el PC compartido. Más el arnés, ~2.5 min.
- **Serie + réplica: 1.1–1.7 h de pared.** La reserva, si hiciera falta: 1 120 corridas, ~25 min.

**Qué no se pudo verificar aquí:**
- el camino con Pool (a un agente no le toca abrirlo; es el mismo patrón `spawn` + `imap_unordered` del runner de v14.3);
- el `__main__` de las baterías copiadas, que necesita estar en `organismo/` (lo prueba la regla 1 al congelar);
- T-H;
- 3T-k (riesgo 7.4).
