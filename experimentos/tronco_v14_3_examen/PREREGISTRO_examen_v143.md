# PREREGISTRO — examen del CRITERIO DE TRONCO v4 sobre v14.3 (= v14.2 + reparación N del nivel 7)

**Escrito ANTES de la serie y ANTES del humo del runner** (23-sep-2026, noche; creador del examen). Antes de escribir esto
sólo se corrió: la construcción por anclas, el arnés de identidad y un cálculo de probabilidades sobre datos **que ya
existían** (`analiza_potencia_v143.py`, no simula un paso). §12 (humo) se escribe después y se dice.
Decisión del director (23-sep, 19:30): *"v14.3 = v14.2 + reparación N del 7; preparar esta noche el examen del criterio v4
para correrlo mañana; congelar si pasa serie y réplica"*. Principio: **el examen v4 es la puerta de NO REGRESIÓN del
organismo común, no un puntaje.** Misión: llegar a la AGI por este camino.
**ENMIENDA ERR-122 (23-sep-2026 ~21:10, ANTES de la serie; decisión del director "corrige la banda"):** la banda de azar G2
de T-B pasa de [0.42, 0.58] a **[0.31, 0.60]** (nulo real del tronco). Detalle y cálculo en §7; cambian §3 (arnés), §4 (fila
T-B), §5 (probabilidades), §10 y §11 (conteos); §12′ trae el arnés y el humo de después. Nada más cambia.

## 1. Hipótesis
**H-v143:** el tronco con la vía lenta normalizada por masa (N) no hace nada peor que v14.2 en lo que el tronco ya hace
(T-A…T-F, en los mundos de la letra) y compone en 3T-k donde v14.2 no (T-G), en semillas nuevas, en serie y en réplica.

## 2. Mecanismo mínimo, memoria y constantes nuevas
- **N (subida_n7, FUNCIONA ×2):** el paso de la vía lenta (`Wps`/`Wns`) se multiplica por `M0 / (P·P)`:
  `_Pl = P*(3.0/float(P@P)) if norm_lenta else P`. Tres líneas y el defecto `norm_lenta=1`. En `organismo_v143cal` (mundo
  vivo) hay dos sitios (la fila de la necesidad activa y las de las otras): se reparan los dos.
- **Memoria nueva: CERO.** **Constante nueva: M0 = 3.0** (la masa de un estímulo en todos los mundos del tronco; no se
  ajusta). El rng no se toca.
- **Inerte por construcción donde P·P = 3** (el factor es 1.0 exacto en punto flotante): el mundo AB del examen v3′, el
  mundo de regla (20 patrones de 3 píxeles), el mundo vivo (PAT A–D) y el bloque de la sal. **Consecuencia que ordena todo
  este preregistro: en T-A, T-B, T-C, T-D, T-E y T-F el candidato ES el tronco v14.2 bit a bit.** Donde actúa: 3T-k
  (masa 3(k+1)) y cualquier mundo con estímulos de masa ≠ 3.

## 3. Instrumento y anclas (todo en `experimentos/tronco_v14_3_examen/`; los orígenes sólo se leyeron)
| archivo | sha16 | origen (sha) | qué es |
|---|---|---|---|
| `organismo_v143.py` | `2cebc0ab0c38b70f` | `organismo/organismo_v142.py` (`17528d767fcebaf6`) | el candidato (a CONGELADOS si pasa) |
| `organismo_v143g.py` | `c20fccaa9107fb89` | `organismo/organismo_v142g.py` (`9e5f566cd6a7a4d2`) | su mundo de regla (a CONGELADOS) |
| `bateria_v143.py` | `9daa88a90a2fd7b1` | `organismo/bateria_v142.py` (`6375d90e531b06e6`) | examen v3′ apuntando a v143 (a CONGELADOS) |
| `bateria_generaliza_v143.py` | `a894101fd1e6db93` | `organismo/bateria_generaliza_v142.py` (`e5929942647756a5`) | + entrada `organismo_v143`, campo a campo (a CONGELADOS) |
| `organismo_v143cal.py` | `1169f54ef0a19de1` | `experimentos/criterio_v3/organismo_v3cal.py` (`148014f68cb01785`) | v14.3 en el mundo vivo (instrumento) |

`construye_v143.py` los genera por anclas, con el **mismo texto** de `subida_n7/construye_n7.py` (`9f5851b9e8ec1ec5`), y
comprueba que el cuerpo de `organismo_v143(g)` es exactamente `subida_n7/organismo_v142N(gN)` (`b5bcff0a4b01c812` /
`d05fc32504cb5517`) con el defecto movido 0 → 1. `--verifica` compara el disco con la construcción.
Reuso por import, con sha fijado en `corre_examen_v143.ANCLAS`: `criterio_v4/corre_criterio_v4` (`c70d1c643e78ee88`, la letra
calibrada y las tareas del tronco en el mundo vivo), `umbrales_v4` (`881e2a07245566bb`), `criterio_v3/corre_criterio_v3`
(`7f93eca0e45e167b`), `nivel11_mundo_vivo/corre_vivo_rep2` (`10ab45355883d98d`), `mini_vivo` (`f3e86cbe6c17e6d7`),
`corre_sal` (`bfdc00bb48656337`), `diagnostico_codigos` (`02905c71a7ac3de8`), `creacion_B/corre_codigo` (`cb91371b77c079d3`),
`tronco_v15_dE5/corre_dE5_v2` (`c042de285398a333`, la letra de T-B/T-C i/T-E/T-F examen), `subida_n7/corre_n7`
(`746e9c70f7beef45`) y `mundo_n7` (`429667c8a334aa48`). Umbrales, semillas y predicciones: `umbrales_examen_v143.py`.
**Arnés `identidad_v143ex.py`: RESULTADO 106/106** (salida en `identidad_v143ex_salida.txt`; bloques en §12). **Tras ERR-122:
114/114** (regla 14 33/33 y el bloque (X) de la enmienda; §12′).

## 4. La letra de CRITERIO_TRONCO_v4, puerta por puerta (ningún umbral tocado salvo la banda de azar G2 de T-B: ENMIENDA ERR-122, §7)
| puerta | medida y montaje | letra (umbral) | n y semillas (serie / réplica) |
|---|---|---|---|
| **T-A** | `corre_vivo_rep2` VIVO y CUELLO_MIN, T = 100 000; brazos OFF (tronco), **CAND**, TRONCO_B (s + 100 000), PLACEBO | muertes ≤ 1.10 ×; `r` ≥ tronco − 10; NI una cola 95 % `LI > −10` (`corre_criterio_v4.letra_TA`) | 80 / brazo: 43101–43180 / 43201–43280 |
| **T-B** | `bateria_generaliza` px0 y azar, T = 200 000, CAND y TRONCO en las mismas semillas; T-B se calcula desde los valores crudos (acc, ba, cobertura), no con el veredicto interno de la batería | G1 ≥ 0.80, G2 ≥ 0.85, azar G1 ∈ [0.35, 0.65], azar G2 ∈ **[0.31, 0.60] (ENMIENDA ERR-122, §7; la de la letra, [0.42, 0.58], se reporta para CAND y TRONCO y no decide)**, K 20/20 | 20: 43001–43020 / 43021–43040 |
| **T-C** | (i) examen E2; (ii) `mini_vivo` VIVO con `invertir_vivo_en = 50 000`, cuatro brazos; `vis[B]`, `vis[A]` por cuarto al lado | (i) come B Q4 ≥ 50 en ≥ 18/20; (ii) NI `LI > −12.5` | (i) 20 como T-B; (ii) 80 como T-A |
| **T-D** | sal muda (`corre_sal.BASE`), OFF y CAND | C1, C2, C6 importados de `creacion_B/corre_codigo.UMBRALES` | 9 ALIAS + 9 LIMPIAS, las **primeras** de 43501–44000 / 44001–44500 (§8) |
| **T-E** | examen v3′, seis etapas, CAND contra TRONCO en las mismas semillas | conducta ≥ 18/20 por escenario, tolerancias 1.10 / 0.8 (`corre_dE5_v2.CLAUSULAS`); pesos reportados | 20 como T-B |
| **T-F** | celdas, divisiones, muertes | ≤ 1.25 × tronco (medianas) en el examen y en el mundo vivo (T-A y T-C ii, divisor `max(tronco, 1)`) | los de T-A, T-C y el examen |
| **T-G** | 3T-k (`corre_n7.tarea`, T = 100 000, k = 1…8), brazos T142 (el tronco), **N** (v14.3) y NC3C (canal falso) | ver abajo | 20: 43401–43420 / 43421–43440 |
| **T-H** | ESCALA | **reportada, no eliminatoria** | **NO SE MIDE**: su instrumento (§5 de la letra) no está construido. Se dice; no se cambia nada |

**T-G, la capacidad que declara el candidato** (la letra la deja al preregistro; se usa la letra de subida_n7 sin tocar un
número, importada de `corre_n7.U`): "compone a k" = T1 `solap_A ≤ 1` en ≥ 15/20, T2 `sep` ≥ 1.5, T3 `lift_q4` ≥ 0.15, T4 el canal
falso no separa, T5 `sep(N) − sep(NC3C) ≥ 1.0` en ≥ 15/20; `K_max` = mayor k con todos los k′ ≤ k componiendo.
**T-G PASA si G-1 `K_max(N) ≥ 5`** (P2 de n7) **y G-2 N > T142 en `lift_q4` pareado en ≥ 15/20 en k = 3, 4 y 5** (GANAR sobre el
tronco; P2 de n7) **y G-3 NC3C con `sep` mediana < 1.0 y `lift_q4` < 0.15 en todo k** (control barajado; P6 de n7).
Nulo, margen y n (regla 15; `analiza_potencia_v143.py` sobre las 40 semillas reales de subida_n7): el **tronco presentado como
candidato** pasa T-G con **0.000** (1000 remuestreos a n = 20; su K_max es 1); G-2 bajo el nulo de signo (p = 0.5) pasa
**0.021**; en el margen (gana en el 85 % de las semillas) pasa **0.933**; con los datos medidos N pasa **1000/1000** (K_max 8 en
todos). n = 20 cumple ≥ 0.95 bajo el nulo y ≥ 0.80 en el margen.
**Por qué T-G es eliminatoria aquí** (la letra dice "una reparación inerte entra como v14.x"): v14.3 es un v14.x, pero declara
una capacidad, y si esa capacidad no se ve en semillas nuevas no hay razón para tocar el tronco. Su probabilidad de caer por
azar es ~0: no añade falso rechazo.
**4′ de la letra:** TRONCO_B y PLACEBO van en T-A y T-C (ii) (las series del mundo vivo que comparan). "Si TRONCO_B no pasa la
letra, la serie no se lee" → **procedimiento declarado ahora** (no es un umbral): esa parte del mundo vivo se corre otra vez en
la RESERVA 43301–43380 (`--reserva --sustituye serie|replica`) y sustituye sólo T-A, T-C (ii) y T-F vivo de esa serie; si la
reserva tampoco se lee, el examen queda NO SE LEE y decide el coordinador con ERR. PLACEBO se reporta (la letra: su paso es
condición de la calibración, no del candidato). T-D no lleva TRONCO_B: no es una comparación, son umbrales absolutos.

## 5. Predicciones firmadas (p = probabilidad de que la puerta PASE en UNA serie; `umbrales_examen_v143.PRED`)
Base: `datos/humo/potencia_examen_v143_20260923_203158.json` (`281b2e55b4ad1aaf`; salida en `analiza_potencia_v143_salida.txt`). Como CAND ≡ tronco en T-A…T-F, se calcula
lo que la letra le hace **al tronco** en 20 (u 80) semillas nuevas.
| puerta | predicción numérica | p |
|---|---|---|
| inercia | CAND == tronco **bit a bit** en todas las corridas de T-A, T-B, T-C, T-D y T-E (lo cuenta el runner) | 1.00 |
| legible | TRONCO_B pasa T-A, T-C (ii) y T-F vivo (reparto del nulo real de V4-CAL: 0.968–0.976; con la reserva ~0.999) | 0.97 |
| T-A | d ≡ 0: LI = 0 > −10 en los dos brazos; razón de muertes 1.000; `r` VIVO ≈ −75 (−85…−65), CUELLO_MIN ≈ −6 (−15…+5) | 1.00 |
| **T-B** | G1 1.000; G2 0.93–1.00; azar G1 0.40–0.60; K 20/20; **azar G2 0.33–0.55 (mediana del tronco 0.434), dentro de [0.31, 0.60] (ERR-122)** | **0.957** (antes de ERR-122: 0.55) |
| T-C | (i) come B Q4 ≥ 50 en 20/20 (el tronco: 60/60, mínimo 51); (ii) LI = 0 > −12.5, `rev` ≈ 43 (30–55) | 0.97 |
| T-D | C1 9/9 (\|W[sal]\| 0.0), C2 9/9 (W[veneno] −3.0), C6 9/9 (el tronco con B-5: 36/36 en dos series) | 0.95 |
| T-E | 20/20 en las seis etapas (sólo pesan E2 "come B ≥ 50" y E2I "tasa A": 60/60 en el tronco) | 0.97 |
| T-F | razones 1.000 exactas | 1.00 |
| T-G | K_max(N) = 8 (rango 6–8), K_max(T142) = 1 (0–2), NC3C 0; N > T142 20/20 en k = 3, 4, 5 | 0.99 |
| **serie** | todas | **0.82–0.91** (antes de ERR-122: 0.47–0.52) |
| **serie + réplica** | **veredicto PASA** | **0.67–0.82** (antes de ERR-122: 0.22–0.27) |

**Cálculo con ERR-122** (sin simular, con los números del mismo JSON `281b2e55b4ad1aaf`; puertas independientes, como en
`analiza_potencia_v143.py`): cota baja por serie = legible 0.9675 × T-B **0.957** × T-C (i)/T-E 0.929 (cota 95 %) × T-D 0.95 ×
T-G 1.000 = **0.817** (= `P_serie_sin_TB` 0.854 × 0.957); cota alta = legible con la reserva 0.999 × 0.957 × 1.000 (60/60) × 0.95
× 1.000 = **0.908**. Serie + réplica = el cuadrado: **0.668–0.825**. (Con P_TB 0.549 las mismas cuentas dan 0.469–0.521 y
0.220–0.271: el rango viejo.)

**Mi predicción del veredicto por la letra, con ERR-122: PASA (p ≈ 0.67–0.82).** El riesgo que queda (0.09–0.18 por serie) se
reparte entre la legibilidad del mundo vivo (la cubre la reserva), azar G1 de T-B (0.969), T-D (0.95 declarada) y la cota
conservadora de T-C (i)/T-E (0.929); ninguno depende de N. *Antes de ERR-122 (texto original, se conserva):* "Mi predicción del
veredicto por la letra: NO PASA (p ≈ 0.75), y casi toda esa probabilidad es T-B — no N. Sin la banda de azar de G2, la serie
pasaría con ~0.85 y el examen con ~0.73."

## 6. Qué significa cada veredicto y qué refuta H
- **PASA** (serie y réplica legibles, siete puertas): v14.3 entra al tronco por el permiso escrito del director → §10.
- **NO PASA**: no se congela; v14.2 sigue siendo el tronco. La lectura depende de **dónde** cae, y el runner lo deja escrito:
  (a) cae una puerta en la que CAND ≡ tronco bit a bit (inercia medida) → **la letra rechaza al propio tronco**: defecto de la
  letra (patrón ERR-91), no de N; se registra con ERR y el director decide. (b) cae T-G → N **no** reproduce la composición en
  semillas nuevas: **refuta H** y reabre subida_n7 (y su +8 del nivel 7). (c) la inercia falla (CAND ≠ tronco en algún mundo de
  T-A…T-F) → **refuta la premisa de §2** (P·P ≠ 3 donde no se esperaba, o un defecto del instrumento): se para y se busca antes
  de leer nada.
- **NO SE LEE**: TRONCO_B cae también en la reserva → ERR; no hay veredicto.
- Vocabulario permitido si PASA: *"la vía lenta normalizada por masa devuelve al tronco la composición en 3T-k (hasta k = 8) sin
  cambiar nada de lo que el tronco hacía (idéntico bit a bit en el examen v4), replicado"*. Prohibido: "razona", "compone
  conceptos", "planifica".

## 7. Riesgo de la LETRA visto antes de correr → ENMIENDA ERR-122 (aplicada el 23-sep-2026 ~21:10, ANTES de la serie)
*Texto original (escrito antes de la decisión; se conserva tal cual). La enmienda va debajo.*

**La banda de azar de G2 de T-B, [0.42, 0.58], está calibrada sobre el azar teórico (0.5) y no sobre el nulo del tronco.** En
las 40 semillas reales del tronco v14.1/v14.2 (101–140) la mediana de azar G2 es **0.434** (series: 0.437 y 0.434, las dos al
borde); a n = 20 la mediana cae dentro de la banda sólo **0.55** de las veces (cuantiles de la mediana: 2.5 % 0.337, 50 %
0.434, 97.5 % 0.550). Es el patrón de ERR-91: una puerta sin su nulo que rechaza al tronco contra sí mismo. La misma banda vive
en `bateria_generaliza` (G2_conducta) desde la Etapa 3 de v9. La letra v4 lo había dejado dicho (§7: "T-B no calibrado con
placebo"). Opciones, **todas antes de la serie**:
- (a) correr con la letra tal cual: P(PASA) ≈ 0.22–0.27 para un candidato idéntico al tronco en ese mundo;
- (b) **ERR nuevo (candidato a ERR-120)** que calibre las bandas de azar de T-B con el nulo real del tronco, como ERR-94 hizo con
  T-A/T-C (ii): con la regla 15 (≥ 0.95 bajo el nulo, las dos bandas juntas) sale azar G2 ∈ **[0.31, 0.60]** (cuantiles 0.5 %–99 %
  de la mediana a n = 20) y azar G1 ∈ [0.35, 0.65] sin cambio: T-B entera pasa **0.957** bajo el nulo (calculado en el mismo remuestreo). Justificación: el nulo, no el candidato. **Advertencia
  honesta:** aquí el candidato ES el tronco en el mundo de regla, así que esto sólo es legítimo si se decide antes de ver la
  serie; después, no.
- (c) una cláusula relativa (azar del candidato frente al tronco en las mismas semillas), que es lo que la puerta quiere decir.
El runner reporta T-B del TRONCO al lado del del candidato, así que si cae se verá que cae igual.

**ENMIENDA ERR-122 (APLICADA; la opción (b)).**
- **Cuándo y quién:** 23-sep-2026, ~21:10. Decisión del director: *"corrige la banda"*. El número lo fija el coordinador
  (ERR-120 y ERR-121 ya se usaron en ECO: el "candidato a ERR-120" de arriba es este ERR-122).
- **Antes de la serie:** no existe ningún dato de serie ni de réplica (la carpeta `datos/` del examen está vacía). Las únicas
  corridas hechas son las del arnés y del humo (semillas 43041–43047 y la ALIAS histórica 326), que no son de ninguna serie, y
  ninguna midió el azar G2 de T-B.
- **Qué cambia:** la banda de azar G2 de T-B pasa de [0.42, 0.58] a **[0.31, 0.60]**. La de azar G1 queda en [0.35, 0.65].
  Todo lo demás de T-B (G1 ≥ 0.80, G2 ≥ 0.85, K 20/20) y de las otras seis puertas: **sin cambio**.
- **Cálculo del nulo** (regla 15; `analiza_potencia_v143.py`, JSON `datos/humo/potencia_examen_v143_20260923_203158.json`,
  `281b2e55b4ad1aaf`): el tronco v14.1 = v14.2 = v14.3 en el mundo de regla, 40 semillas reales 101–140; mediana de azar G2
  **0.4344**; remuestreo de la mediana a n = 20 (B = 20 000): cuantiles 0.5 % 0.3028, 1 % 0.3184, 99 % 0.5974, 99.5 % 0.6033.
  La banda [0.31, 0.60] (dos decimales, entre esos cuantiles) deja pasar a **T-B entera (las cinco cláusulas juntas) 0.957**
  bajo el nulo, en el mismo remuestreo (≥ 0.95). Con [0.42, 0.58] eran 0.549.
- **Dónde vive:** `umbrales_examen_v143.ERR122` y `NUM['TB_azar2']`. `corre_examen_v143.veredicto_TB` calcula T-B desde los
  valores crudos de la batería (acc, ba y cobertura por semilla) con esa banda. No usa el veredicto interno de
  `bateria_generaliza`: la congelada `bateria_generaliza_v142.py` y su copia `v143` conservan su banda interna [0.42, 0.58] y
  no se tocan. `regla14()` compara todo lo demás con los módulos de origen y registra `TB_azar2` como diferencia DECLARADA por
  ERR-122, no como falla (33/33).
- **Por qué no favorece al candidato:** la banda se aplica igual al CAND y al TRONCO (v14.2 congelado en las mismas semillas;
  en T-B no hay TRONCO_B, porque la letra 4′ lo pone sólo en el mundo vivo). En T-B el candidato ES el tronco bit a bit, y el
  runner lo cuenta. El runner reporta T-B de los dos con la banda nueva y, **sólo como informe**, con la vieja: en el log de la
  etapa 2, en la línea T-B de la etapa 8 y en `--combina`. La banda nueva contiene a la vieja: todo lo que pasaba sigue pasando.
- **Qué cuesta:** la puerta deja de detectar un azar G2 entre 0.31 y 0.42 o entre 0.58 y 0.60, que es donde cae el propio
  tronco en ~45 % de las series de 20. Fuera de [0.31, 0.60] sigue diciendo NO (arnés (X): 0.30 y 0.61 caen).
- **Arnés y humo después de la enmienda:** §12′.

## 8. Semillas NUEVAS (buscadas el 23-sep ~21:00; `busca_semillas_v143.py`, salida en `busca_semillas_v143_salida.txt`)
| papel | serie | réplica |
|---|---|---|
| examen v3′ y T-B | 43001–43020 | 43021–43040 |
| mundo vivo T-A y T-C (ii) (comparten semillas: mundos distintos, como V4-CAL) | 43101–43180 (TRONCO_B 143101–143180) | 43201–43280 (TRONCO_B 143201–143280) |
| T-G 3T-k | 43401–43420 | 43421–43440 |
| T-D ALIAS (primeras 9 con \|code(D)∩code(B)\| = 3) | 43568 43572 43575 43605 43626 43647 43654 43712 43748 (de 43501–44000) | 44031 44099 44119 44138 44185 44218 44237 44242 44291 (de 44001–44500) |
| T-D LIMPIAS (primeras 9 con \|D∩B\| = 0) | 43505 43522 43528 43529 43539 43541 43551 43556 43571 | 44004 44005 44015 44016 44017 44020 44022 44025 44027 |
| reserva del mundo vivo (sólo si TRONCO_B no pasa) | 43301–43380 (TRONCO_B 143301–143380) | |
| humo / identidad | 43041–43044 (+ la ALIAS histórica 326) / 43045–43047 | |

La búsqueda recorrió 24 331 archivos de texto de `PROYECTOS/JUACO` (repo, los ocho worktrees, sandbox, respaldo): en
43000–44600 y 143000–144600 sólo aparecen sellos de hora `HHMMSS` en nombres de archivo (p. ej. `_043921`, `_143636`),
fragmentos de sha (`219aa43408de5393`, `dc058e0a43216bf3`, `d043870f88f5b9c8`) y una URL; **ningún uso como semilla**. La
selección de T-D es estructural (`diagnostico_codigos.solapamientos`, sin simular) y el runner la recalcula y se para si no
coincide. Ninguna semilla coincide con V4-CAL (2361–2440, 2841–2940), subida_n7 (7701–7799) ni tronco_v14_3 (14281–14340).

## 9. Las cuatro trampas
1. **Canal simétrico:** no hay canal entre organismos; en T-G el canal falso NC3C (historia aleatoria con el mismo formato) es el
   control barajado. 2. **Acierto sin balancear:** G1/G2 son balanceados (½ comida + ½ veneno); en 3T-k `lift = acc − base`
   descuenta la tasa base. 3. **El mundo que se come la comida:** `rev` con `vis[B]`, `vis[A]` por cuarto al lado; mordidas y
   muertes en 3T-k; exposiciones a la sal en T-D. 4. **Sitios fijos:** el mundo vivo y 3T-k reponen en posiciones sorteadas;
   celdas y divisiones reportadas (T-F).

## 10. Procedimiento de congelado si el examen PASA (ESCRITO, no ejecutado: lo ejecuta el coordinador con el permiso del director)
1. `python manifiesto.py --check` → 20 intactos. `python experimentos/tronco_v14_3_examen/construye_v143.py --verifica` → todo igual.
2. Copiar **byte a byte** a `organismo/`: `organismo_v143.py`, `organismo_v143g.py`, `bateria_v143.py`, `bateria_generaliza_v143.py`
   (no se regeneran: se copian los que examinó el examen) y comprobar sus sha: `2cebc0ab0c38b70f`, `c20fccaa9107fb89`,
   `9daa88a90a2fd7b1`, `a894101fd1e6db93`. `organismo_v143cal.py` **no** entra al tronco (instrumento del examen, como
   `organismo_v3cal`); se recomienda fijar su sha como ancla de los exámenes futuros bajo v4.
3. Con la llave `JUACO_CONGELAR=1` puesta por un humano (NUBE.md §4; la guardia bloquea editar `manifiesto.py` sin ella), pegar al
   final de `CONGELADOS`:
   ```python
       # v14.3 = TRONCO desde el <fecha> (examen del CRITERIO DE TRONCO v4: PASA en serie y replica; permiso del director 23-sep 19:30).
       # v14.3 = v14.2 + REPARACION N (norm_lenta; subida_n7 FUNCIONA x2): el paso de la via lenta x M0/(P.P), M0 = 3.0.
       # Memoria nueva CERO; constante nueva M0 = 3.0; rng intacto. Inerte por construccion donde P.P = 3 (identidad_v143ex
       # 114/114; examen v4: CAND == v14.2 bit a bit en T-A..T-F). Donde actua (3T-k): compone hasta K_max 8; v14.2, hasta 1.
       # Examen con la banda azar-G2 de T-B enmendada por ERR-122 ([0.31, 0.60], antes de la serie; decision del director).
       './organismo/organismo_v143.py':          '2cebc0ab0c38b70f',
       './organismo/organismo_v143g.py':         'c20fccaa9107fb89',
       './organismo/bateria_v143.py':            '9daa88a90a2fd7b1',
       './organismo/bateria_generaliza_v143.py': 'a894101fd1e6db93',
   ```
   `python manifiesto.py --check` → **24** intactos.
4. **Regla 1 nueva** (CLAUDE.md, regla de trabajo 1 y bloque de estado; con Pool, la corre el coordinador, con `--log` para que
   las dos baterías copiadas ESCRIBAN su JSON en `organismo/`, ERR-42):
   `cd organismo && python bateria_v143.py 6 && python bateria_generaliza_v143.py organismo_v143 20 --desde 101`
   (histórica: `bateria_v142.py 6` y `bateria_generaliza_v142.py organismo_v142 20 --desde 101`; v14.1, v13, v11, v9). Debe salir
   todo PASA con los mismos números que v14.2 (es el mismo organismo en esos mundos). ERR-122 enmienda la puerta T-B del examen,
   no la batería: `bateria_generaliza_v143` conserva su banda interna [0.42, 0.58] (en 101–120 el tronco da 0.437, dentro).
5. `CLAUDE.md` (tronco v14.3 + regla 1), `ESTADO.md`, entrada del REGISTRO ("CONGELACIÓN v14.3 … coste 0 % en el tronco por
   identidad, no por medida; compone en 3T-k hasta 8"), commit y
   `git tag -a v14.3-tronco -m "v14.3 = v14.2 + N (via lenta normalizada por masa, M0 = 3.0, memoria nueva cero). Examen v4 PASA en serie y replica; identico a v14.2 bit a bit en T-A..T-F; compone en 3T-k hasta K_max 8."`
   y `git push origin v14.3-tronco`.
6. Si algo de 1–4 falla: **no se congela**, se registra con ERR y v14.2 sigue siendo el tronco.

## 11. Comandos y costo (sólo el coordinador; los agentes no corren `--serie`, ERR-115)
Antes de cada serie el runner corre el arnés (se para si no da 114/114, tras ERR-122), la regla 14 (33/33) y la selección de T-D.
- **Nube** (4 núcleos; Pool 3 = nproc − 1; bits idénticos al PC):
  `/root/venv-juaco/bin/python experimentos/tronco_v14_3_examen/corre_examen_v143.py --serie --pool 3`
  `/root/venv-juaco/bin/python experimentos/tronco_v14_3_examen/corre_examen_v143.py --replica --pool 3 --con experimentos/tronco_v14_3_examen/datos/examen_v143_serie_<sello>.json`
- **PC** (Pool 6, con los otros Pools parados o dentro del tope de 14 procesos):
  `python experimentos/tronco_v14_3_examen/corre_examen_v143.py --serie --pool 6` y
  `python experimentos/tronco_v14_3_examen/corre_examen_v143.py --replica --pool 6 --con <JSON de la serie>`
- Sólo si una serie NO SE LEE: `... --reserva --sustituye serie|replica --pool N`; y `... --combina <serie> <replica> <reserva>`.
- Si el análisis se cayera después de las corridas (los crudos ya están en disco, ERR-54): `... --analiza experimentos/tronco_v14_3_examen/datos/examen_v143_<modo>_<sello>` rehace el veredicto sin correr nada (probado con crudos
sintéticos fuera del repo, igual que `--combina`).
- **Costo por serie:** 1 796 corridas (T-B 80 de T = 200 000; examen 240; T-D 36; T-C ii 320; T-A 640; T-G 480).
  Humo (un proceso, PC menos cargado): mundo vivo 5.5–5.9 s, examen 4.6 s, 3T-k 4.8 s por corrida de T = 100 000 → **2.8 h de CPU**.
  Bajo Pool con el PC cargado (tiempos reales de V4-CAL y subida_n7: mundo vivo 8.8–9.1 s, 3T-k 7.1 s) → **4.2 h de CPU**.
  **Pared por serie: PC con Pool 6 ≈ 30–45 min; nube con Pool 3 (núcleo 1.3–2.2× más rápido) ≈ 30–50 min**; + arnés ~3 min.
  **Serie + réplica: 5.6–8.4 h de CPU, 1–1.6 h de pared.** La reserva (si hiciera falta): 960 corridas, ~2.3 h de CPU, ~25 min.

## 12. Humo y arnés (UN proceso) — escrito DESPUÉS de §1–§11
**Arnés `identidad_v143ex.py` → RESULTADO 106/106** (190 s, con el runner final; `identidad_v143ex_salida.txt`; JSON
`datos/humo/identidad_v143ex_20260923_204757.json`, `9a5c9055bb741098`): (0) construcción 6/6 · (A) N apagada == v14.2 12/12 ·
(I) N encendida == v14.2 12/12 · (B) mundo de regla 6/6 · (C) mundo vivo 11/11 · (D) tareas del runner 5/5 · (E) reproduce el crudo
de subida_n7 4/4 · (R) regla 14 32/32 · (J) el juez reproduce a dE5, V4-CAL y subida_n7 5/5 · (K) controles 13/13. La primera corrida
dio 105/105; después añadí un control más (bandera desconocida con un modo válido) y exigí código 2 de argparse: 106/106. Los
controles del parser llaman sólo a `argumentos()` en el mismo proceso, nunca a `main()`: el arnés no puede lanzar una serie.
**Humo `corre_examen_v143.py --humo`** (12.6 s; 6 corridas: cinco de T = 20 000 y una de 100 000; JSON
`datos/humo/examen_v143_humo_20260923_204303.json`, `1c419a0eb2b1a308`; el primer humo, 20:35, dio los mismos números antes
de añadir `--analiza` y el formato a prueba de `None` en dos líneas de log). **No es dato:**
| corrida | resultado |
|---|---|
| T-A VIVO s43041, OFF y CAND | r −22 / −22, muertes 23 / 23: **CAND == OFF bit a bit** (inercia en el mundo vivo) |
| T-C (ii) CAND s43042 | rev 17, visB [389, 103, 65, 34] |
| T-D CAND ALIAS 326 (histórica) | \|W[sal]\| 0.02, W[veneno] −2.95 a T = 20 000 (B-5 actuando: 6 divisiones por R = 0) |
| examen E2 CAND s43043 | come B en Q4 88 (≥ 50) |
| T-G N k = 5 s43044 | sep 3.659, lift_q4 0.216 |
Cableado de la etapa 8 con crudos sintéticos de tamaño real: el candidato idéntico al tronco **pasa las siete**; el MALO (r y rev
−40, azar 0.30, \|W[sal]\| 1.45, sin componer) **cae T-A, T-B, T-C, T-D y T-G**. Regla 14 32/32; selección de T-D recalculada == la
declarada.
**Qué no se pudo verificar aquí:** el camino con Pool (a un agente no le toca abrir Pool; es el mismo patrón `spawn` +
`imap_unordered` de los runners del repo); el `__main__` de las baterías copiadas, que necesita estar en `organismo/` (lo prueba la
regla 1 con `--log` al congelar, §10.4); T-H.

## 12′. Arnés y humo DESPUÉS de la enmienda ERR-122 (UN proceso; escrito después, 23-sep ~21:35)
**Arnés `identidad_v143ex.py` → RESULTADO 114/114** (191 s; `identidad_v143ex_salida.txt`; JSON
`datos/humo/identidad_v143ex_20260923_213414.json`, `1005dabb2fc053f7`): (0) 6/6 · (A) 12/12 · (I) 12/12 · (B) 6/6 · (C) 11/11 ·
(D) 5/5 · (E) 4/4 · (R) **33/33** (la comprobación de T-B se parte en dos: G1, G2 y azar G1 == origen; azar G2 = diferencia
DECLARADA por ERR-122) · (J) 5/5 (a dE5 se lo juzga con la banda vieja, la que usó su juez, y también pasa con la nueva: azar G2
0.532) · **(X) 7/7** (la banda que decide es [0.31, 0.60] y el resto de T-B no cambia; la vieja == origen y las baterías conservan
su banda interna; con azar G2 0.36 PASA con la nueva y la vieja dice NO sólo como informe; bordes: 0.30 NO, 0.31 y 0.60 PASA, 0.61
NO; el log, la etapa 8 y `--combina` muestran la vieja como SOLO INFORME para CAND y TRONCO) · (K) 13/13.
**Humo `--humo`** (12.9 s, 6 corridas; `datos/humo/examen_v143_humo_20260923_213425.json`, `740de61f78bb8384`): las seis corridas
dan los mismos números que el humo de las 20:43 (T-A VIVO CAND == OFF, r −22; rev 17; |W[sal]| 0.02; come B 88; T-G N k = 5, sep
3.659 y lift 0.216): la enmienda no toca la simulación. Cableado: el bueno pasa las siete; el MALO cae T-A, T-B (0.30 < 0.31),
T-C, T-D y T-G; con ERR-122 (azar G2 0.36 en CAND y TRONCO), T-B PASA con la nueva y la vieja dice NO sin decidir. Regla 14
33/33. No es dato.
