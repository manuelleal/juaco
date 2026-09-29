# PREREGISTRO (EXPLORATORIO) — BLOQUES_PISTA: genoma de reglas heredable evolucionando DENTRO de la pista de la carrera (28-sep-2026, creador)

Misión: llegar a la AGI por este camino. Principio del director: que la evolución construya el órgano, no nosotros, y sólo con selección natural.
**Todo es EXPLORATORIO** (5 semillas, T 100 000, sin Pool). Decide sólo si se escribe el esqueleto del intento #7 del muro.
Escrito con el arnés pasado y el humo LANZADO, antes de mirar cualquier número del humo o de la exploración.

## 0. Verificación previa (pedida): ¿la retina y las letras de la pista permiten que una regla de rechazo separe lo malo?
- Las letras NO cambian de significado por semilla: `pista.cfg_fabrica()` deriva de `organismo_f9c` fijo: A comida (+0.8 E), B veneno (−0.4 E),
  C agua (+0.8 Ag), D sal (−0.4 Ag); `nec_shuf 0`, `pat_shuf 0`, `invertir_en None`. Retina fija (6 píxeles):
  A = 110100 · B = 101010 · C = 011001 · D = 001011. **Píxel 4 = 1 sólo en B y D; píxel 1 = 0 sólo en B y D**: una regla de una condición
  ("píxel 4 > θ → boca −w") separa exacto lo malo de lo bueno. No hace falta leer la memoria R. Arnés (C): la regla forzada baja las mordidas
  B+D 63 → 11 (T 2000, s 59292).
- **PERO** (sonda termo_organo, coordinador 21:05): el anillo es ~90 % B+D; morder lo malo LIMPIA el camino a la comida; el rechazo de ECO
  pegado a TERMO hunde al linaje (R0 0.87 → 0.13; el fundador muere de hambre). El órgano útil en la pista no es "no muerdas B/D" sino
  "cuándo limpiar y cuándo comer". Por eso: (1) el genoma NO arranca con el rechazo; (2) se agrega el **sentido 6** = cercanía del objeto más
  cercano del anillo con píxel j (lo que hay alrededor, sin significado de letra), junto a hambre y sed; (3) se mide A+C en el anillo
  (telemetría del linaje 0 cada 5000) y `frac_sin_bueno_mundo`.

## 1. Hipótesis
Si el carro TERMO lleva un genoma de reglas componibles heredable (hijo = padre mutado; refundador = entrada del banco del linaje, donde sólo
entra quien parió), la selección dentro de la pista arma reglas que bajan la mortalidad del fundador y los fundadores por linaje, y el R0 real
sube hacia O1 (P1 del muro: mayoría que cruza en ≥ 15/20).

## 2. Mecanismo y memoria nueva (construye_bp.py; carros V143_BQ, V143_BQAZA, V143_BQ0)
Port por lectura de `bloques/opusM/motor_bloques.py` a la interfaz de carro. Regla = (sentido 0–6, j, comparador, θ, acción 0 boca / 1 patas /
2 quedarse, w ∈ [−3, 3]); ≤ 12 reglas. Operadores: campo p 0.10 por regla, dup 0.02, del 0.07, ins 0.05; INICIAL 2 reglas al azar si el banco
del linaje está vacío; banco 50 por linaje. Sin HGT entre linajes (sería un canal fuera del reglamento). Sin acción "parir" (la decide la pista).
rng = `ctx['rng']` del carro (revisa_carro prohíbe rng propio). Memoria nueva: la lista de reglas + última letra mordida y su R por cuerpo.
**Tasas escaladas respecto de opusM (ins 0.02 → 0.05, INICIAL 0 → 2)**: la pista tiene 9 cuerpos a la vez, no 90–3000; declarado.

## 3. Brazos (9 carros iguales, L 360, T 100 000, fundador limpio = ENMIENDA 5, entrada = corre_termo.tarea)
| brazo | carro | papel |
|---|---|---|
| termo | V143_TERMO | base (MODESTO ×2, R0 0.93) |
| bloq | V143_BQ | CANDIDATO: reglas heredables + banco del linaje |
| bloqaza | V143_BQAZA | CONTROL que puede fallar: mismas tasas, sin herencia (cada cuerpo sale de una entrada al azar del banco de listas NUEVAS) |
| o1 | O1 | ancla |
Semillas NUEVAS (grep 21:00): exploración 59201–59205 · humo 59291 · arnés 59292. Pasajes: no (no hay tiempo antes de las 23:00; declarado).

## 4. Predicciones (firmadas antes de ver números)
| # | predicción | p |
|---|---|---|
| B1 | humo: rechazo forzado (s 59291, T 20k) tiene R0 real mediano < termo (reproduce la sonda) | 0.75 |
| B2 | fundadores por linaje (media de 9) bloq < 0.7 × termo en ≥ 3/5 semillas | 0.25 |
| B3 | R0 real (mediana de 9) bloq > termo en ≥ 4/5 semillas | 0.25 |
| B4 | bloq > bloqaza en R0 real en ≥ 4/5 | 0.35 |
| B5 | bloqaza < termo en R0 real en ≥ 3/5 (reglas al azar estorban) | 0.55 |
| B6 | mayoría que cruza bloq ≥ 4/5 | 0.10 |
| B7 | el órgano de rechazo puro aparece en el banco final de ≥ 1/3 de los linajes de bloq | 0.10 |
| B8 | o1: mayoría que cruza 5/5 | 0.75 |

## 5. Lectura (exploratoria)
**NOS ACERCAMOS** = B3 y B4 y (B2 o fundadores mediana bloq < termo en ≥ 4/5). **NO** = cualquier otra cosa con arnés y corridas completas.
**NO APLICA** = arnés falla o abortos. Control que puede fallar: si bloqaza mejora igual que bloq, no es herencia sino el sesgo de las reglas.

## 6. Qué lo refuta
bloq no supera a termo en R0 y fundadores, o no supera a bloqaza.

## 7. Añadido 20:59 (ANTES de ver cualquier número a T 100k; sólo el humo T 20k estaba leído): PASAJES
Por si la selección dentro de UNA corrida no alcanza (en el humo sólo 11/280 fundadores de bloq salieron del banco: los linajes que fallan
nunca paren y su banco queda vacío). Cadena c = 1..5: 4 pasajes a T 25 000 en las semillas 59220 + 4(c−1) + p (p = 0..3; 59220–59239 libres
al grep); la siembra del pasaje siguiente = unión de los bancos finales de los 9 linajes (en bloq sólo entra quien parió); cada linaje arranca
con 50 listas al azar de la siembra (rng del RUNNER). Luego PRUEBA a T 100k en la semilla 59200 + c (la misma de termo/o1: pareado).
Brazos `bloq_pas` y `bloqaza_pas` (control: la misma transferencia, sin herencia dentro del pasaje).
| # | predicción | p |
|---|---|---|
| B9 | R0 real bloq_pas > termo en ≥ 4/5 | 0.30 |
| B10 | bloq_pas > bloqaza_pas en ≥ 4/5 | 0.35 |
| B11 | fundadores por linaje (media) bloq_pas < bloq (sin pasajes) en ≥ 3/5 | 0.40 |
| B12 | mayoría que cruza bloq_pas ≥ 4/5 | 0.10 |
NOS ACERCAMOS (pasajes) = B9 y B10 y fundadores (media o mediana) bloq_pas < termo en ≥ 4/5.

## 8. Añadido 21:13 — v2 (DESPUÉS de leer la exploración v1 de termo/bloq/bloqaza, ANTES de cualquier número v2 o de pasajes)
Lectura v1 que lo motiva (declarada): bloq ≈ termo (R0 pareado 2/5, −0.14; fundadores media 127.8 vs 125.4); el fundador muere a ~43–83 pasos
por veneno+sal (98–99 %); ninguna regla fijada se parece a un órgano (deriva). O1 sólo PRUEBA lo desconocido con E y Ag > 0.5. Con los
sentidos v1 una regla no distingue "desconocida" de "conocida": eso está en la memoria del linaje (`_adS`, ya en v14.3).
v2 (`construye_bp2.py` desde V143_BQ / V143_BQAZA por anclas): **sentido 7** = la letra en foco ya fue mordida por el linaje (1/0, lee `_adS`,
cero memoria nueva); **sentido 8** = reserva min(E, Ag). Todo lo demás igual. Carros V143_BQ2 (padre) y V143_BQ2AZA (azar).
- **Diagnóstico humo2 (NO es candidato; es "mi instinto a mano" como en opusM):** la regla PRUEBA de O1 escrita en reglas, forzada, tasas 0:
  "desconocida → boca −3" + "reserva > 0.5 → boca +3", en 59201–59203, T 100k. Sirve para saber si la gramática v2 CONTIENE una solución.
| # | predicción | p |
|---|---|---|
| C1 | prueba_forzada: fundadores por linaje (media) < 0.5 × termo en ≥ 2/3 semillas | 0.50 |
| C2 | prueba_forzada: R0 real > termo en ≥ 2/3 | 0.45 |
| B13 | bloq2 > termo en R0 real en ≥ 4/5 | 0.20 |
| B14 | regla "prueba" (sentido 7 u 8, `<`, boca, w < 0) en el banco final de ≥ 1/3 de los linajes de bloq2 | 0.20 |
| B15 | bloq2 > bloq2aza en ≥ 4/5 | 0.30 |
Si C1 y C2 fallan, la gramática no contiene la solución de O1 y B13 se da por perdida de antemano.

## 9. Resultado (21:40; EXPLORATORIO, 59201–59205, T 100k; lectura `datos/explora_T100000/lectura.txt`, `resumen_bp.json`)
**NO.** Ningún brazo de reglas se separa de TERMO; ninguna regla converge entre linajes; el genoma se queda en el largo inicial (2.0): deriva.
| brazo | R0 real (med. por semilla) | mayoría cruza | fund./linaje media · mediana | establecidos | fund. muere veneno+sal · vida med | pareado R0 vs termo |
|---|---|---|---|---|---|---|
| termo | 0.773 | 2/5 | 125.4 · 5 | 33/45 | 99 % · 43 | — |
| bloq | 0.816 | 1/5 | 127.8 · 6 | 31/45 | 98 % · 83 | 2/5 (−0.14) |
| bloqaza | 0.655 | 0/5 | 147.2 · 3 | 27/45 | 94 % · 148 | 1/5 (−0.12) |
| bloq_pas (4 pasajes 25k) | 0.758 | 2/5 | 121.0 · 7 | 29/45 | 99 % · 49 | 1/5 (−0.03) |
| bloqaza_pas | 0.721 | 2/5 | 122.1 · 11 | 28/45 | 95 % · 98 | 2/5 (−0.05) |
| bloq2 (sentidos 7, 8) | 0.750 | 2/5 | 128.1 · 1 | 30/45 | 98 % · 84 | 2/5 (−0.17) |
| bloq2aza | 0.731 | 1/5 | 134.9 · 6 | 25/45 | 92 % · 134 | 1/5 (−0.13) |
| prueba_forzada (diagnóstico, 3 sem.) | 0.957 | 3/3 | 155.1 · 1 | 24/27 | 99 % · 46 | 1/3 (−0.00) |
| o1 | 0.944 | 5/5 | 26.5 · 0 | 40/45 | 97 % · 200 | 4/5 (+0.16) |
A+C en el anillo (mediana, linaje 0 cada 5000): 3–4 de 36 objetos. bloq vs bloqaza 3/5 (+0.06); bloq2 vs bloq2aza 2/5 (−0.12); bloq_pas vs bloqaza_pas 3/5.
Predicciones: B1 sí (humo, n 1) · B2 NO · B3 NO · B4 NO · B5 sí · B6 NO · B7 no ocurrió (0/45) · B8 sí · B9 NO · B10 NO · B11 sí (4/5) pero
bloqaza_pas < bloqaza en 5/5: es el pasaje, no la herencia · B12 NO · C1 NO (155 > 125) · C2 NO (1/3) · B13 NO · B14 NO (0/45) · B15 NO.
Sin esqueleto del intento #7: no hay señal que preregistrar.

## 10. Ronda 2 (21:55, antes de cualquier número): más material para la selección
- ¿Más población sin tocar pista.py? **No existe.** `pista.N_MAX = 9` y un cuerpo vivo por linaje; `escala` y `mundo_n` sólo cambian el TAMAÑO del
  mundo (L = 40·M, nobj = 4·M), no el número de cuerpos. Entonces sólo tiempo: **T 300k** y **pasajes largos** (3 × 100k, siembra = unión de los
  bancos, prueba a T 300k).
- Brazos: termo, bloq2, bloq2aza (sentidos v2: alrededor, conocida, reserva) en 59401–59403 (594xx libre al grep 21:52); bloq2_pas y bloq2aza_pas:
  pasajes en 59410 + 4(c−1) + p (c 1..3, p 0..2), prueba en 59400 + c. Carros SIN cambios (arnés §9 vale; sólo cambian semillas y lectura).
- Medida nueva: regla FIJADA = tipo de regla (sentido, j, comparador, acción, signo) en ≥ 50 % de los 9 vivos de la última muestra.
| # | predicción | p |
|---|---|---|
| D1 | alguna semilla de bloq2 (T 300k) con regla fijada | 0.15 |
| D2 | bloq2_pas con regla fijada en ≥ 2/3 | 0.30 |
| D3 | fundadores mediana bloq2_pas < termo en ≥ 2/3 y R0 real > termo en ≥ 2/3 | 0.15 |
| D4 | bloq2_pas > bloq2aza_pas en R0 en ≥ 2/3 | 0.35 |
HAY SEÑAL = D3 y D4 y regla fijada en bloq2_pas ≥ 2/3 que no aparece en bloq2aza_pas.

## 11. Resultado ronda 2 (22:43; EXPLORATORIO, 59401–59403, T 300k): **NO**
| brazo | R0 real (mediana por semilla) | mayoría cruza | fund./linaje mediana · media | establecidos | regla en ≥ 50 % de los vivos | R0 vs termo |
|---|---|---|---|---|---|---|
| termo | 0.926 | 2/3 | 4 · 347 | 19/27 | — | — |
| bloq2 | 0.804 | 1/3 | 17 · 386 | 16/27 | 0/3 (máx. 0.22) | 1/3 (−0.00) |
| bloq2aza | 0.884 | 1/3 | 19 · 360 | 16/27 | 0/3 | 1/3 (−0.10) |
| bloq2_pas (3 × 100k) | 0.754 | 1/3 | 28 · 315 | 13/27 | **1/3** (0.89: "píxel 4 del foco < 0.5 → patas hacia lo que mira +") | 1/3 (−0.23) |
| bloq2aza_pas | 0.984 | 2/3 | 1 · 343 | 15/27 | 0/3 | 1/3 (−0.00) |
Bancos tras el pasaje 2 (lee_siembra.py, datos/pasajes_Tp100000_np3_sp59410/siembras.txt): con herencia la regla más frecuente llega a
0.67 / 0.21 / 0.27 de las listas; sin herencia 0.09 / 0.10 / 0.25. La única fijación (c1: "acercarse a lo que no tiene píxel 4" = ir hacia A/C)
coincide con el PEOR R0 (0.41; fundadores mediana 123). D1 NO · D2 NO (1/3) · D3 NO · D4 NO (0/3).
