# Índice de `experimentos/`

> Foto al **21-sep-2026**, **actualizado al 23-sep-2026** (filas del 21–23-sep añadidas por el cronista y revisadas por el coordinador) (redactado por el cronista Sonnet desde los `PREREGISTRO_*.md` / `PROPUESTA*.md` / `README.md` de cada carpeta,
> `registro/REGISTRO_etapas_1_2.md` y `registro/HANDOFF.md`; revisado por el coordinador). Se actualiza en cada `/juaco-cierre` cuando
> nace o cierra una carpeta. Fechas por sello de archivo. "Sin registro" = no hay entrada que cite la carpeta o su instrumento en
> REGISTRO ni HANDOFF; no es lo mismo que "no corrió". Los números de línea (L) son del REGISTRO al 21-sep y se desplazan al añadir.

| carpeta | nivel/etapa del brief (como lo usa el registro) | fechas | qué se midió | veredicto registrado | dónde | estado |
|---|---|---|---|---|---|---|
| `dia1_exploracion` | 0 — pre-Etapa (exploración previa al protocolo) | 15-sep | Búsqueda manual del organismo mínimo (sim.py→vida.py→retina→morder→organismo v4→población) | Sin PASA/CAE (fase que originó el método); hallazgo: "el hambre rompe el mínimo local de huir también sirve" | HANDOFF §1 | cerrado |
| `etapa2` | Etapa 2 (pre-protocolo; ramas 2, 2A–2L) | 15-sep | Inversión del mundo A↔B en t=50k, 12 semillas, un cambio por vez | Mixto: 2G "extinción 12/12" confirmatorio; 2M (pulpo) REFUTADA; 2L candidato a v7 | REGISTRO L27–L156 | cerrado |
| `etapa3` | Etapa 3 (pre-protocolo, generalización) | 15-sep | Sonda `organismo_v6_sonda.py`: valor a priori de 64 patrones vs. solapamiento Kenyon | PASA con autocrítica: 100 % de 1 280 pares dentro de 0.15; diseño "casi tautológico" | REGISTRO L280 → L376 | cerrado |
| `bug01` | — (BUG-01, defecto de tronco heredado de Etapa 2) | 15–16-sep | Decaimiento en Wp/Wn, coste del arreglo, coste con techo mordiendo | Exp.1 REFUTADO; Exp.2 CONFIRMADO (mecanismo) pero P1 REFUTADA; ahorro A1/A5 REFUTADAS (ERR-11); coste con techo PASA 14/14 | REGISTRO L613, L696, L981, L1267 | cerrado |
| `congelacion_v8` | — (congelación v8, criterio v3) | 16-sep | Examen de congelación v8 | **PASA — v8 tronco** | REGISTRO L1446 | tronco histórico, superado |
| `ramas` | 2 / 3 / 7 (2K-bis capacidad, 3K Kenyon, 3T temporal) | 15-sep | 2K-bis: capacidad ante solapamiento; 3K: ¿hace falta que Kenyon aprenda?; 3T: composición temporal | 2K-bis converge con BUG-01; **3K REFUTADA** ("basta el azar"); **3T confirmatorio: NO** | REGISTRO L449, L575, L651 | cerrado |
| `etapa2_politica` | Etapa 2 (2P, frontera hambre/supervivencia) | 16-sep | Frontera entre explorar con hambre y sobrevivir, sobre v8 | No pasa como estaba escrita; cambia el problema; 20 % de la vida parado sobre el veneno | REGISTRO L1675 | cerrado |
| `v9_memoria_rechazo` | Etapa 2 (cierre) / tronco v9 | 16-sep | v9 = v8 + memoria de trabajo de rechazo | **PASA M0–M6, examen 20/20 — v9 tronco**; Etapa 2 cerrada | REGISTRO L1836, L1894 | tronco histórico, superado |
| `etapa3_v9` | Etapa 3 (sobre v9) | 16-sep | Generalización dura en valor y conducta | **G1 y G2 SOSTENIDAS — Etapa 3 cerrada** | REGISTRO L1933, L1984 | cerrado |
| `v11_generaliza` | Etapa 3 / nivel 7 (re-verificación sobre v11) | 17-sep | "Generalización = interferencia" en 20 semillas; 3T sobre v11 | D1–D4 SOSTENIDAS; 3T sobrevive; generalización NO (v11 es un canje) | REGISTRO L2437, L2501 | cerrado |
| `nivel3_asociacion` | nivel 3 (asociación por parecido) | 18-sep | B-4: ¿asocia en una exposición donde el parecido predice el valor? | **NO CONFIRMA como estaba escrito**: acelera en general, no específicamente | REGISTRO L4434 | cerrado |
| `creacion_A` | nivel 3 (XOR) + candidatos a tronco v15c–v15f | 17–18-sep (+ ERR-87 el 21-sep) | Candidatos XOR (xor_3f→xor_7) y memoria de pares en la vía lenta (v15c–v15f, vector único) | xor_3f ANULADO; **xor_7 (M3) CIERRA la línea XOR** (1.000 ×2); v15c/d/e NO ENTRAN; v15f NO ENTRA por v1, primer candidato del criterio v2; vector único CONFIRMADO (60/60) | REGISTRO L4652, L4730–L5154 | XOR cerrado / **v15f-v2: serie corriendo desde el 21-sep 12:37** |
| `enjambre` | nivel 3 (XOR, sala de 19 agentes; grupos M1–M4) | 18-sep | Pilotos de 3 semillas de 4 mecanismos para XOR | M1 y M2 REFUTADOS; M3 (memoria de un golpe) no refutado → confirmatoria en `creacion_A/xor_7`; M4 sin refutación | HANDOFF §15.8.3 | borrador (pilotos) |
| `etapa4_v9` | Etapa 4 (memoria persistente, sobre v9) | 16-sep | Ausencia con interferencia, herencia | **NO se cierra: olvido catastrófico** | REGISTRO L2073 | cerrado (negativo) |
| `v10_direccion_division` | Etapa 4 (`mu` normalizada) | 16-sep | Confirmatorio + examen de v10 | Réplica (b) FALLA: **v10 NO es tronco**, instrumento | REGISTRO L2380 | cerrado (instrumento) |
| `v11_consolidacion` | Etapa 4 (spec K6, auto-repaso) | 16-sep | Sólo `ESPEC_exploracion_autorepaso.md`; sin preregistro ni scripts | Sin registro (K1–K5 corrieron en otra carpeta) | REGISTRO L2137 | **borrador huérfano** |
| `evo` | — (JUACO-EVO, evolución guiada por LLM) | 16–17-sep | 4 mutaciones LLM + 4 ciegas, control ciego | Gen 1: `llm_2` (conflicto de signo) R 1.0 vs 0.3/0.4 — hipótesis; ERR-18 corregido | REGISTRO L2269, L2306 | cerrado (alimentó v11) |
| `v11_evo_division` | Etapa 4 (cierre) / tronco v11 | 17-sep | v11 = v10 + división por conflicto de signo | Examen 8/8; **v11 tronco**; Etapa 4 cerrada en 4 estímulos | REGISTRO L2385–L2386 | tronco histórico, superado |
| `v12_ceguera_graduada` | Etapa 4 (canje retención/generalización, 6 β) | 17-sep | Ceguera graduada de la hija | **H SOSTENIDA** (ningún β logra ambas); `hija-madura` REFUTADA | REGISTRO L2554 | cerrado |
| `v13_dos_vias` | Etapa 4 (rompe el canje) / tronco v13 | 17-sep | Dos vías (rápida + lenta) | P4 CONFIRMADO, P5 sostenida; X1 falla → tras arreglar el control **v13 tronco** (101–120) | REGISTRO L2602, L2664, L2718 | tronco histórico, superado |
| `nivel4_puerta_codigo` | nivel 4 (puerta por evidencia del código, B-2) | 18-sep | Capacidad de v11 sin perder generalización | Recupera capacidad (N* 50.5 vs 35); réplica 121–140 **8/8 → v14** | REGISTRO L4060, L4121, L4279 | tronco (en v14) |
| `creacion_B` | nivel 4 (B-5 desambiguar) + construcción v14.2 | 17–18-sep | ¿Se repara el alias con división por R = 0? | Réplica **PASA — DECLARADO**; v14.2 congelado | REGISTRO L4865, L4916, L5462 | tronco (v14.2) |
| `etapa5_comunicacion` | Etapa 5 (N1–N3) | 16–17-sep | Señal innata, significado emergente, sentidos complementarios | N1-asimétrico **DEMOSTRADO** (réplica 21–40); N2 **REFUTADO ×6, CERRADO**; **N3d TRANSFIERE** (0.811 vs 0.516); N3d mudo: obedece, no enseña | REGISTRO L2179, L2856, L3181–L3685 | cerrado |
| `creacion_C` | nivel 5 (N2 por predicción, C-P6) | 17–18-sep | ¿Aprende el receptor por predicción o sólo obedece? | Primera serie NULA; réplica **sin resultado firme** | REGISTRO L4578, L4608 | cerrado (sin resultado) |
| `junta_fase5` | fase 5 (familia Y variante, en el mundo del nivel 12) | 19-sep | Tres creadores Opus A/B/C | **C NO (×2); B NO (×2); A NO (sin réplica)** — fase 5 en 75 % | REGISTRO L5472–L5491; HANDOFF §15.12 | cerrado; **candidato B+A en diseño (`BA/`, 21-sep)**; `C/PREREGISTRO_oreja.md` no corrido |
| `nivel6_mapa` | nivel 6 (dirección hacia comida recordada) | 17-sep | ¿Elige la dirección hacia comida que no ve? | **REPLICADO** | REGISTRO L3070 | cerrado |
| `nivel6_rodeo` | nivel 6 (dos metas y rodeo) | 17-sep | Elegir entre dos comidas y rodear veneno recordado | Primera serie sin declarar (validez); con enmienda 1, 61–80 **REPLICADO** | REGISTRO L3636, L3660 | cerrado |
| `nivel6_2d` | nivel 6 (2D) | 18-sep | Rodeo real, rodeo falso, encadenar, horizonte 2 | **NO rodea, se aleja**; rodeo falso confirmado (0.05); encadena mejor borrando el sitio comido; horizonte 2 sin potencia | REGISTRO L3942 | cerrado |
| `nivel7_3T_k` | nivel 7 (historias de k pasos) | 17-sep | ¿Compone k pasos? | **REPLICADO k = 1, 2, 3**; k = 4 no replica con gemelo | REGISTRO L3048, L3207, L3470 | cerrado |
| `nivel7_hija_dispersa` | nivel 7 (B-1 hija dispersa) + v13D | 17–18-sep (+ ERR-87 el 21-sep) | ¿Compone mejor con menos celdas? No regresión | Primera serie CAE por la letra (16/20); réplica 81–100 **PASA**; v13D no regresiona 8/8 → v14 | REGISTRO L3725, L3805, L3989 | tronco (en v14) |
| `nivel7_xor_lectura` | nivel 7 (XOR: ¿lectura o representación?) | 17-sep | Vía cuadrática, regla fusionada, oráculo de rasgos | Cuadrática representa pero no clasifica; 3d REFUTADA; 3e tampoco (0.625): "el cuello es la DINÁMICA" | REGISTRO L3274, L3296, L3514, L3588 | cerrado |
| `3T_confirmatorio` | nivel 7 (control transversal sobre v8) | 16-sep | ¿La división descubre sola la dimensión del orden? | Primera NO (ERR-13); corregido **SÍ**; réplica 21–40 **SÍ** | REGISTRO L1505, L1547, L1597 | cerrado |
| `v9_reverificacion` | transversal sobre v9 | 16-sep | 3T y 2K-bis sobre v9 | Los dos sobreviven | REGISTRO L2003 | cerrado |
| `v13_reverificacion` | transversal sobre v13 | 17-sep | 3T y capacidad sobre v13 | 3T sobrevive; **capacidad cae** como se predijo (ERR-22) | REGISTRO L2745 | cerrado |
| `capacidad_grande` | transversal sobre v11 | 17-sep | Retina 10 px, 60 estímulos | G1 y G2 sostenidas; **G3 (XOR) REFUTADA** | REGISTRO L2398 | cerrado |
| `nivel8_curiosidad` | nivel 8 (curiosidad por progreso de error) | 17-sep | ¿Recupera la exploración que pierde el mapa? | **REFUTADA** | REGISTRO L3251 | cerrado |
| `nivel8_novedad_sitio` | nivel 8 (novedad de sitio) | 17-sep | Sesgo por tiempo desde la última visita, dos dosis | Dosis 0.6 refutada; 1.8 casi; réplica 81–100 **cae — línea cerrada** | REGISTRO L3356, L3422 | cerrado |
| `nivel8_escala_mapa` | nivel 8 (saturar el valor recordado) | 17-sep | ¿Libera exploración? | **REFUTADA**; canje **ESTRUCTURAL**: v14 sin mapa | REGISTRO L3556 | cerrado |
| `nivel8_metaplasticidad` | nivel 8 (A-2 masa de conflicto) | 18-sep | ¿Frena el olvido de lo ausente? | **REFUTADA** (0.667 = base; muere 73 % más) | REGISTRO L3760 | cerrado |
| `nivel8_mundo_largo` | niveles 8–9 (mundo largo, cambio sin aviso) | 17-sep | v13 vs v13+mapa, 50 patrones | Veredicto compuesto NO; hallazgos: techo de retina ~0.8, recupera en ~2000 pasos, el mapa daña la adquisición | REGISTRO L3152 | cerrado |
| `nivel9_allostasis` | nivel 9 (rama exploratoria, modelo de sí mismo) | 17-sep | Predictor de ΔE que modula eta | P1 NO; P3 OK: "la sorpresa no acelera; el predictor mide" | REGISTRO L3612 | cerrado (exploratorio) |
| `nivel9_probar_si_mismo` | nivel 9 (C-P1 sorpresa en la boca, dE-TEST) | 18-sep (+ ERR-87 el 21-sep) | ¿Probar cuando no me reconozco acelera la recuperación? | **REPLICADO** (0.26×, 0.22×); dosis 10 pierde G1; **dosis 5 cumple todo ×2** → "dE5 después" | REGISTRO L3839–L4186 | **candidato pendiente (dE5)** |
| `nivel10_composicion_v14` | nivel 10 (composición de candidatos) | 18-sep | Hija dispersa + puerta (+ dE-test) | Dos: réplica **8/8 → v14**; tres: **NO van juntos** (7/8) | REGISTRO L4160–L4241 | tronco (2) / no entra (3) |
| `nivel11_mundo_vivo` | nivel 11 (necesidades, propósito, reproducción, muerte) | 18-sep | Núcleo, alias, reproducción, H-1 | Núcleo replicado; **alias CONFIRMADO**; bloque 2 (r) **DECLARADO**; **H-1: el mundo NO sostiene linajes mortales** | REGISTRO L4671–L5349 | cerrado (H-1 en pie) |
| `nivel12_mundo_familias` | nivel 12 (familias y variantes) | 18-sep | Bloques 0–6 | B0 insatisfacible (ERR-45); B1 INDECISO; B2 REPLICADO (linealidad); B3 v15f indeciso; B4/4b nada por la letra; B5 nada (nivel 5 → 70 %); **B6 REPLICADO** (nivel 5 → 75 %) | REGISTRO L5154–L5453 | cerrado; sigue en `junta_fase5` |
| `externo_codex` | nivel 12 (sufijo de variante, pieza de Codex) | 18-sep | Sufijo de 3 píxeles en la tabla de pares | Integrado en el bloque 6: REPLICADO | REGISTRO L5430 | cerrado |
| `nivel13_alma` | nivel 13 (ALMA: curitas guiadas y nodo) | 18-sep | 20 almas Haiku vs azar / nodo barajado; borrador "eras" | **El alma razonada NO gana al azar** (0.525); el contenido del nodo sí (0.88); ningún linaje llega a R₀ 0.9 | REGISTRO L5404 | cerrado; `PREREGISTRO_eras.md` con humo de 1 semilla, sin serie |
| `externo_mundo_minimo` | — (réplica del mundo mínimo de ChatGPT) | 18-sep | ¿Soporta memoria episódica? | Calibración reproducida; sin acción no prueba memoria (predicción cumplida); con acción R₀ 0.96 → 1.86 | REGISTRO L5339 | cerrado |
| `lateral_exoesqueleto` | — (línea lateral: exoesqueleto de un LLM) | 18-sep | EXO-1 y EXO-2, humos 901–906 | Sin registro aquí: la línea salió a su **propio repo `PROYECTOS\JUACO-EXO` (alefast)** el 19-sep, con sus resultados | REGISTRO L5458; commit 40dba2e | cerrado aquí (vive en alefast) |
| `aprende_barrer` | fase 9, bloque 3 (camino A) | 22–23-sep | APR (boca aprendida, heredada) vs FABRICA vs APR_SIN_HERENCIA vs APR_AZAR; serie 8101–8120, réplica 8121–8140 (sólo APR y FABRICA) | **HAY ALGO MODESTO, REPLICADO** — APR gana a FABRICA 20/20 en las dos series (+0.051 / +0.049); en la serie gana a APR_SIN_HERENCIA 20/20 (+0.094); no descubre la limpieza; no cruza (0.387 / 0.385) | REGISTRO L6330 y entrada del 23-sep | cerrado (modesto replicado) |
| `carrera_escuderias` | — (transversal; alimenta nivel 9) | 22-sep | reglamento (9 escuderías 3O/3S/3H, meta R0 ≥ 0.90); rondas 0, 1 (sellada) y 2 (combos Opus, sellada) | ronda 0 sin ganador (0.332); ronda 1 **primer cruce de H-1** replicado en sellada (R0 real 0.941); ronda 2 **O3 y O4 ganan y estabilizan con muerte programada declarada, replicado**; O2 estabiliza sin ganar | REGISTRO L6159, L6303, L6355 | cerrado (ronda 2) |
| `carrera_fase10` | — (carrera nocturna A/B/C del 21-sep) | 21-sep | tres caminos independientes hacia el mundo de fase 10 | Sin registro propio; lo integrado va en `nivel10_mundo_acumula` | Sin registro | sin cerrar |
| `criterio_v3` | — (criterio de tronco v3) | 21-sep | calibración CAL-1..CAL-5 y réplica | calibración PASA; réplica NO REPITE → v3 no utilizable | REGISTRO L5878, L5947 | retirado el 22-sep |
| `criterio_v4` | — (criterio de tronco v4, ERR-94) | 22-sep | V4-1..V4-5, serie 2841–2920 y réplica 2361–2440 | **UTILIZABLE** en serie y réplica; v3 retirado | REGISTRO L6217 | criterio vigente |
| `diagnostico_muro` | fase 9 (H-MURO) | 22-sep | P1–P4, semillas 2941–2946 | **H-MURO SE SOSTIENE**; el pastoreo selectivo existe pero no es la causa principal | REGISTRO L6135 | cerrado |
| `escuela` | — (EXPLORATORIO, escuela de abejas) | 22-sep | sin preregistro ni arnés | **EXPLORATORIO, no es dato** — aprende XOR sólo con detector de pares; la sabia ayuda por copia (muleta) | HANDOFF §15.30 | exploratorio |
| `generaciones` | fase 9/10 (generaciones que conviven, pista v2) | 22–23-sep | pista v2 + quimiostato; monocultivos 10101–10120 | 22-sep: instrumento (37/37), ERR-104; 23-sep: monocultivos **en curso** | REGISTRO L6379; HANDOFF §15.31 | en curso |
| `junta_20260921` | nivel 5 (BA-vm / BA-vM) | 21-sep | junta de tres creadores Opus | **CAE por la letra** (P3, P4, R6); BA-vm cruza P6 pero muere 9.6× la base | REGISTRO L6028; HANDOFF §15.12 | cerrado |
| `mundo_anclado` | fase 9 (toxicidad + dilución) | 22-sep | v1 y v2: calibración, confirmación, réplica | v1 **NO**; v2 **HAY ALGO MODESTO** (se sostiene con reservas, ERR-111..113) | REGISTRO L6243, L6266 | cerrado con reservas; pendiente fila tox 2.0 |
| `nivel05_familia_variante_BAv` | nivel 5 | 21-sep | BA-v en tres series bajo ERR-90 | **CAE P6 en las tres** (13/19, 14/18, 11/16); colisión estructural con la hermana | REGISTRO L5630; HANDOFF §15.22 | cerrado |
| `nivel06_rodeo_obligado` | nivel 6 | 21-sep | mundo muralla, serie 1702–1721 | **CAE (5/10)**; réplica no se corre | REGISTRO L5913 | cerrado; lo retoma `subida_n6` |
| `nivel07_fanin_expansion` | nivel 7 (fanin 6/3/2) | 22-sep | serie 6021–6040, réplica 6041–6060 | **CAE la hipótesis del director**, replicado; la conjunción mejora con menos entradas (no predicho) | REGISTRO L6185 | cerrado |
| `nivel09_cuerpo_nuevo` | fase 9, bloque 1 | 21-sep | F9-1..F9-10; series 1501–1520, 1521–1540, 1621–1640 | **núcleo del bloque 1 DECLARADO** con dos series válidas; ni el ORÁCULO cruza R0 0.9 | REGISTRO L5651, L5716, L5835, L6095 | declarado |
| `nivel09_cuerpo_nuevo_b2` | fase 9, bloque 2 | 21-sep | 14 puertas; serie 1581–1600, réplica 1601–1620 | **F9-4bis replicado ×2**; C-F9B′ cerrado | REGISTRO L5980, L6055, L6095 | declarado |
| `nivel10_mundo_acumula` | nivel 10 (mundo de fase 10) | 22-sep | integración del instrumento (F0 79/79, sonda 11/11) | sin dato, instrumento listo | REGISTRO L6109 | instrumento listo |
| `tesoro` | — (EXPLORATORIO, bits con pizarra) | 22-sep | sin protocolo | **EXPLORATORIO, no es dato** — con pizarra 12/12, sin ella 2/12; falta examen sin pizarra | HANDOFF §15.30 | exploratorio |
| `tronco_v15_dE5` | nivel 9 (dE5 bajo criterio v2) | 21-sep | T-A..T-G, semillas 2001–2080 | **NO ENTRA** (caen T-A, T-C ii, T-E, T-G) | REGISTRO L5690; HANDOFF §15.19 | cerrado |
| `subida_n5` | nivel 5 (V-5: familia Y variante en la misma tabla) | 23-sep | arnés 33/33; humo 25791 | preparado, sin serie (un arranque accidental del auditor se abortó en 40/840; log en `datos/humo_no_registrado/`, no es dato) | HANDOFF §15.31 | preparado (LISTO CON CORRECCIONES) |
| `subida_n6` | nivel 6 (mundo que sí obliga a rodear) | 23-sep | arnés 42/42; humo 6641 | preparado, sin serie | HANDOFF §15.31 | preparado (LISTO CON CORRECCIONES) |
| `subida_n7` | nivel 7 (3T-k sobre el tronco v14.2) | 23-sep | arnés 114/114; mini-prueba: el tronco no compone a k≥3 (posible regresión) | preparado, sin serie | HANDOFF §15.31 | preparado (LISTO CON CORRECCIONES) |
| `subida_n8` | nivel 8 (aprendizaje abierto con 90 celdas) | 23-sep | arnés 26/26; humos 12690–12691 | preparado, sin serie; en auditoría | HANDOFF §15.31 | preparado |
| `subida_n9` | nivel 9 (¿O3 cruza porque se lee a sí mismo?) | 23-sep | arnés 22/22; lesiones H-SI / H-RES | preparado, sin serie | HANDOFF §15.31 | preparado (LISTO CON CORRECCIONES) |
| `subida_n10` | niveles 10–13 (el nodo viaja en el parto, pista v2) | 23-sep | arnés 26/26; humo 12391 | serie 12301–12320 **en curso** | HANDOFF §15.31 | en curso (LISTO PARA SERIE) |

## Borradores y huérfanos (sin preregistro o sin corrida ni entrada)
- `v11_consolidacion`: sólo una especificación; nunca se convirtió en preregistro.
- `nivel13_alma/PREREGISTRO_eras.md`: instrumento y runner listos, humo de 1 semilla, sin serie.
- `junta_fase5/C/PREREGISTRO_oreja.md`: escrito, "NO corrido" por su autor.
- `enjambre`: pilotos de humo; la confirmatoria vive en `creacion_A/xor_7`.

## Paquetes verificados pendientes de correr (al 21-sep)
1. `creacion_A/corre_v15f_v2.py` — **corriendo desde el 21-sep 12:37** (Pool 10).
2. `nivel9_probar_si_mismo` dE5 — decisión del director: después de v15f.
3. `nivel13_alma/PREREGISTRO_eras.md` — sin decisión.
4. `junta_fase5/C/PREREGISTRO_oreja.md` — sin decisión.

## Convención de nombres
Conviven cuatro: `nivelN_*` (niveles del brief), `etapaN_*` (terminología pre-protocolo), `vN_*` (versión del tronco, no nivel) y
`creacion_X` / `junta_faseN` / `enjambre` (por equipo de agentes). La ambigüedad más dañina: `v12_ceguera_graduada` (tronco v12) y
`nivel12_mundo_familias` (nivel 12) comparten número sin relación. **Desde el 21-sep, carpetas nuevas:** `nivelNN_<tema>_<candidato>`
(dos dígitos) cuando el bloque ataca un nivel del brief; `tronco_vNN_<tema>` cuando es congelación, confirmatorio o re-verificación de una
versión del organismo. Nada de lo existente se renombra (los runners y el registro citan las rutas actuales).
