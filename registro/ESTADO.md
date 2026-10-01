> **Ruta de publicación:** ver `registro/RUTA.md` (casilla actual y siguiente paso).

# ESTADO: una página que se reescribe en cada cierre (skill `/juaco-cierre`)

> Última reescritura: **1-oct-2026, ~15:00** (cierre de la jornada del 1-oct, antes del apagado de las 16:00), por el coordinador. Rama `organelos`, todo commiteado y empujado (cierre del 1-oct). Lo exploratorio vive aparte en `exploratorio/` (ver su `LEEME.md`).
> Sin merge a `main` (lo decide el director). Detalle en `REGISTRO_etapas_1_2.md` ("Jornada del 1-oct-2026") y en `experimentos/organelos/escalera/ESCALERA.md`.

## Tronco
**v14.3** (tag `v14.3-tronco`) sigue siendo el tronco. Candidato v14.4: TERMO′ (sólo cae T-E). Sin cambios.

## Lo declarado (serie + réplica)
1. **★★ ESCALERA P1, memoria de lugar: FUNCIONA ×2.** 79 y 85 linajes de 180 contra 0 del control antípoda, 20/20 ×2.
2. **★ ESCALERA P7, señal con significado dado entre linajes clones, con costo: FUNCIONA ×2 con reserva (ERR-175).** 132 y 124 contra 80 del mudo y 50 del control.
3. **★★ ESCALERA P10, ir a lo menos visitado cuando el oasis se muda: FUNCIONA ×2.** 164 y 163 de 180; mayoría en 20/20 ×2; R0 0.96.
4. **★★ ESCALERA PISA, la señal leída puede pisar memoria de lugar caducada: FUNCIONA ×2 con reservas** (serie en el umbral). Latencia mediana de los lectores 973.5 y 982.5 pasos contra 1317.8 y 1205.5 de la variante apagada (pmix < mix 15/20 y 17/20; razón 0.78 ×2; contenido 16 y 17/20; explorador mudo 20 y 19/20). Reservas: el mundo A+C no es igual (7.8 contra 6.3); con el explorador mudo y un mundo igual de rico es más lento que la variante apagada con explorador que habla; el cruce de lectores mejora (140 y 143 contra 117 y 126 de 160) pero no depende de que el explorador hable; rumor 15.8–18.2 % sin daño medido.
5. **★★ ESCALERA P8, celda retenida: COMP2 FUNCIONA ×2 y COMP2 MEJORA ×2 con reservas (ERR-179, ERR-190).** D mediana 0.75 ×2, D > 0 en 20/20 ×2, permutada 0; COMP2 mejora a COMP 17/20 y 20/20 (+0.50). **COMP: serie MODESTO, réplica NO: no se declara.** Reservas: la afirmación máxima del preregistro (suma y compuerta cableadas, memoria de lugar con bono en los bins del oasis); "E le gana a una A visible dentro del oasis" (la E sola se muerde 57 % fuera en todos los brazos); "A sobre E sólo a igual lugar" (mismo bin 0.99; entre bins distintos 0.72 y 0.70: con la puerta vieja sería NO); no se detecta costo de cruce y no se descarta (comp2 97 contra lug 113 sumando serie y réplica); mundo A+C 7.5 contra 6.3.
6. **NO ×2 — "los tres juntos" NO SUMAN** (preregistro `1b5e483f`). Cruzan de 180: todo 159 y 169, memoria + ir a lo menos visitado 163 y 163, memoria + señal 129 y 129, sólo memoria 88 y 95, los tres con la señal al antípoda 90 y 95. La señal no agrega cruce sobre memoria + ir a lo menos visitado; su contenido sí importa.
7. **NO — réplica de moneda_muro (ERR-177):** el CONSERVA del explora no replicó (fracción INDETERMINADO: moneda 0.0 contra neutra 0.42; cruce SIN DIFERENCIA: 41 contra 42 de 90). Auditoría: se sostiene.

Todo lo de la Escalera es DISEÑO DIRIGIDO (ingeniería genética sobre O1) y vale **en el mundo con oasis (que se muda)**. No es selección ni el muro de la pista vieja. Vocabulario: "tres módulos diseñados, cada uno contra un control de contenido equivocado; juntos no suman". No decir "comunicación", "lenguaje", "aprende", "inventa", ni "×2" donde no hay réplica.

8. **★★ ESCALERA, perillas: FUNCIONA ×2 (una evidencia, no dos; letra cumplida fuera del umbral en la serie y en la réplica, 0 abortos): en el mundo con oasis de P1, la selección por persistencia sube desde cero la perilla del viaje de la memoria de lugar (GV mediano 0.19 ×2 contra 0.02 y 0.0 de la deriva; sel > neu + 0.05 en 19/20 y 20/20) y el genoma que deja la selección cruza más que el de la deriva (sel 79 y 70 contra neu 14 y 7 de 180; O1 6 y 4) y algo menos que el diseño (fab 80 y 83; en la réplica sel contra fab gana 5, empata 4, pierde 11, sin significación pareada). Reservas: sel deja el mundo A+C más pelado que O1 (4.32 y 4.44 contra 7.03 y 6.95), parte de la ventaja puede venir de vaciar el oasis; el módulo lo escribió el ingeniero y la selección sólo prende su perilla; queda en el primer escalón (GV ≈ 0.19), no en el diseño.** Es la única línea del proyecto, con el órgano de rechazo de BLOQUES y ECO_SEL, donde la SELECCIÓN hace el trabajo; aquí sobre un módulo diseñado.

## El muro de la pista vieja (H-1): sigue en pie; qué sabemos ahora
- **La selección conserva a O1, no lo mejora, con reloj mutacional corto** (o1_libre ≈ 12 eventos; o1_evo y entre_linajes de orden 20–30, una serie, genes limitados): o1_evo 128 contra 81 del neutro, pero 128 contra 135 de fábrica; visto también en entre_linajes y en o1_libre. El reloj de selección entre linajes no está medido (F0, AUDITORIA_F0).
- **La moneda (exploratorio, 5 cadenas; NO REPLICÓ el 1-oct, ERR-177):** con pasajes de 25k la selección purga la regla que cruza (0.26 contra 0.64). Con 100k y siembra de establecidos el explora dio CONSERVA en el umbral y la réplica (n = 10, `4f07e7f0`/`200e0d0a`) dio INDETERMINADO. "La moneda era un candado" queda RETIRADA como causa.
- **El montaje tenía defectos medibles:** genoma BQ2 clavado en 2 reglas (Δlargo 0), carga mutacional ~0.11 por regla y generación, Ne de linajes ≈ 9 (1/Σp², máximo 9; no es un Ne genético).
- Las piezas de O1 sueltas no funcionan; O1 funciona como conjunto (29-sep).
- **Perillas, sonda `regimen` (exploratoria, n = 2):** el mundo pelado de la selección lo causa un GV intermedio (viajero a medias), no GW; la selección llegó al primer escalón donde el módulo paga, no al diseño; el diseño es igual o mejor por persistencia. No es un tramposo del pozo común.
- **Hipótesis del bien público (SIN MEDIR):** el genetista propone que el gen perdido es el NIVEL de selección: la limpieza es un bien público que la selección entre linajes dentro de un mundo mezclado no sostiene. Su firma en `o1_evo` NO SE PUEDE LEER. Se prueba con dos cámaras, mixta contra clonal.
- **Mapa del muro por genes de O1 (`muro_perillas/`, exploratorio, 1–2 semillas, nada se declara; arnés 33/33):** MARGEN (el margen de la boca) es una RAMPA en dos semillas (0 → 0 y 0; 0.03 → 0 y 4; 0.06 → 3 y 8; 0.10 → 8 y 9 de 9). Desde todo apagado, MARGEN solo ya da 5/9 y la limpieza suma sólo con MARGEN puesto (7/9): escalera con orden, no valle a ciegas. PISO, PEN_OTRO y PRUEBA sin tendencia. **Candidato ERR-191 (no abierto):** con fundador limpio la pista regala limpieza (cada refundador prueba B y D una vez); por eso O1 sin limpieza cruza 5/9 con fundador limpio y 0/180 con fundador no limpio. En pista mixta se ve el costo del único que limpia (R0 0.002 y 0.004, ×2 semillas) pero no el beneficio del polizón.

## La Escalera (`experimentos/organelos/escalera/ESCALERA.md`, `BITACORA.md`)
| peldaño | estado |
|---|---|
| P0 unicelular (O1) | hecho |
| P1 memoria de lugar | **FUNCIONA ×2** |
| P7 señal con costo | **FUNCIONA ×2** (reserva ERR-175) |
| P10 ir a lo menos visitado | **FUNCIONA ×2** |
| los tres juntos | **NO SUMAN ×2** |
| PISA: la señal puede pisar memoria caducada | **FUNCIONA ×2** (reservas; serie en el umbral) |
| perillas: la selección sube la perilla del viaje (GV) desde cero | **FUNCIONA ×2** (19/20 y 20/20; cruzan 79 y 70 contra 14 y 7 del neutro; fab 80 y 83; o1 6 y 4); **mundo A+C 4.32 y 4.44 contra 7.03 y 6.95 de O1**; una evidencia, no dos; primer escalón (GV 0.19), no el diseño |
| P8 celda retenida | **COMP2 FUNCIONA ×2 y MEJORA ×2** (reservas, ERR-179, ERR-190); **COMP NO** (serie MODESTO, réplica NO) |
| P9 planear | **LIBERADO sin construir:** ESPACIO NO (sondas: piso 8, oráculo 6, azar 6, regalo 6 de 18) |
| P2 colonia pegada | CERRADO en ráfaga (5 humos) |
| P3–P6 germen/soma, órganos, nervio, cerebro | diseñados, sin correr (dependen de P2 o de ECO grande) |
| Tramo D sexo y familia | instrumentado; sin señal: el mundo de 9 no tiene población para familias |

## Otras sesiones
- **JUACO 5 (rama `o1-libre`, commit `23a6c83d`; no es nuestra, sólo se cita):** O1 libre con poderes: **BLOQUE NO** (la subida de MEM, 10/10 en la serie con dif 0.0596, no replicó: 6/10, dif 0.047). Se repite sólo que la selección sostiene a O1 frente a la deriva en ≈ 12 eventos mutacionales por cadena; vale para ese reloj, no para evolución larga. **No decir** "la selección elige la memoria de lugar". F2 "un gen por parto": **NO** (la carga se quitó, neutro R0 0.97, pero lib 57 contra O1 72). Cierre en `experimentos/organelos/o1_libre/CIERRE_o1_libre.md` (rama o1-libre). JUACO 5: bloque 160–169, usó el 160.
- **Investigación y exploración (fuera de protocolo, irá en `exploratorio/`):** F0 (reloj mutacional ≈ 12 eventos; reloj de selección no medido), Reactor (costo lineal, 0.40 × escala de vivos; paso 0: un órgano funcional fijado, segundas funciones 0–2/40), borrador F1 (esc 90 contra esc 900, para el PC nuevo), espec P9 (liberado por las sondas), gen perdido, bloques autoentrenables; `red_celulas/` (con techo justo no gana en aprender ni en readaptarse; el pago por camino chico elimina al tramposo); `alejo/` (documento de arranque del proyecto Alejo, dos perspectivas).
- **Revisión de solo lectura de "Juaco revisión":** los cuatro FUNCIONA ×2 previos (P1, P7, P10, juntos NO SUMAN ×2) se sostienen; las frases de F0 y la numeración de ERR ya están corregidas aquí.

## PLAN DE LA PRÓXIMA SESIÓN (el PC se apaga a las 16:00; en orden; cada uno con su preregistro commiteado antes y pool total ≤ 6)
1. **Perillas del muro: MARGEN como gen desde cero en la pista vieja**, con el montaje de perillas (cámara continua, una mutación por parto, δ 0.01, dos relojes medidos). Es el mejor camino al muro que ha habido: hay rampa en dos semillas y un montaje que ya funcionó ×2. Antes: completar la semilla 2 del mapa y repetirlo con fundador NO limpio; fijar `GEN_LETRA = MARGEN` en `muro_perillas/corre_muro_perillas.py` y en su preregistro; auditor; commit; serie + réplica (~3.2 h cada una con pool 2).
2. **Fundador limpio (candidato ERR-191):** decidir qué hacer con la prueba de B y D del refundador (la pista regala limpieza por nacimiento), revisar qué series viejas usaron cada regla, y sólo entonces leer algo sobre limpieza. Comandos del mapa: `python experimentos/organelos/muro_perillas/corre_muro_perillas.py --mapa --lote C2` (también B2, D2) y `--lee`; un proceso por lote, el runner se niega con 6 python ocupados.
3. **Dos cámaras, mixta contra clonal, para el gen de limpieza** (ficha 3 del genetista; hipótesis del bien público, hoy sin medir). Preregistro antes; el control puede ganar.
4. **Perillas con reloj más largo o δ menor:** ¿la selección llega al diseño (GV → 1, mundo sin pelar) o se queda en el primer escalón? La sonda `regimen` dice primer escalón; reloj y nulos nuevos antes de correr.
5. **Varios módulos apagados a la vez en el mundo que se muda** (memoria de lugar, señal, ir a lo menos visitado, PISA como genes desde cero): ¿la selección prende más de uno? Recordar "una evidencia, no dos" y el mundo A+C.
6. **Reactor F1 en el PC nuevo** (borrador v2: esc 90 contra esc 900; base del paso 0: un órgano fijado en 38/40, segundas funciones en 0–2/40; costo lineal).
7. **Alejo (proyecto aparte, experimento 2):** empezar por la perspectiva A. Lo exploratorio del 1-oct apunta ahí: la "hamburguesa" (modelo congelado + células de memoria viva sobre su estado interno) funciona en juguete; la red de células como modelo propio no gana con rival justo. Paso siguiente: modelo abierto pequeño de verdad, compuerta adaptativa, RAG por embeddings como rival, 20 semillas + réplica, criterio de abandono escrito. Todo en `exploratorio/investigacion_20261001/` (`alejo/ALEJO.md`, `red_celulas/`).
No hacer: más vueltas de pasajes de 25k contra el muro; piezas sueltas de O1; leer nada sobre limpieza sin resolver lo del fundador limpio.

## Niveles (los fija el director)
+2 por el termostato-en-la-pista ×2 (aceptado el 29-sep; total +17–22). Sin cambio hoy: PISA ×2 y P8-COMP2 ×2 son diseño dirigido en un mundo propio (como P1, P7 y P10); perillas ×2 es selección sobre un módulo diseñado; el NO de moneda_muro retira una explicación. Decide el director al leer.

## ERR
Esta sesión usó el 30-sep: ERR-157, 158, 159 y 170 a 176. Hoy: **ERR-177** (método: lo exploratorio "en el umbral" no se escribe como causa hasta réplica), **ERR-178** reservado a perillas y **no usado**, **ERR-179** (enmienda de la puerta A sobre E de P8), **ERR-190** (instrumento: `_spearman` de P8 sin promediar empates; no cambia veredictos). 180–189: bloque de la sesión de investigación. JUACO 5: bloque 160–169 (usó el 160). ERR-191 es CANDIDATO (fundador limpio regala limpieza), no abierto. **Siguiente libre de esta sesión: ERR-191 si se abre el candidato; si no, 191.**

## Decisiones del director de hoy (1-oct)
- El PC se apaga a las **16:00**.
- **Alejo es el experimento 2** del director; el nombre es el de su hijo (Joaquín Alejandro). JUACO es el primero.
- **Explorar las ideas antes de refutarlas.**
- El correo a Discovery Loop **sigue en espera** (no enviar hasta saber si aceptan el póster en Bucaramanga).

## Decisiones pendientes para el director (máximo 2)
1. Merge de `organelos` (y de `o1-libre`) a `main`, y qué entra a `RESULTADOS_VERIFICADOS.md` (lo toca la sesión de publicación). PISA ×2 y P8-COMP2 ×2 llevan reservas que deben viajar con el titular.
2. Qué se lleva al PC nuevo primero: perillas del muro sobre MARGEN (recomendado), el Reactor F1 (esc 90 contra esc 900), o Alejo-A con un modelo abierto pequeño.
