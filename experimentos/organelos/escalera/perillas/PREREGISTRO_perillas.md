# PREREGISTRO — ¿LA SELECCIÓN PRENDE LO QUE EL MUNDO PAGA? Las perillas de la memoria de lugar como genes que arrancan en cero, en el mundo con oasis de P1 (perillas, CONFIRMATORIO, 1-oct-2026)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).
Encargo del director (1-oct, mañana). Creador: Fable. Carpeta nueva `experimentos/organelos/escalera/perillas/`; nada de `escalera/` ni de `o1_evo/` se editó
(se importan por sha). **Escrito DESPUÉS del arnés (74/74), de dos humos y de dos exploraciones de un proceso (sec. 11, `../BITACORA.md`; nada de eso
cuenta) y ANTES de cualquier dato de serie.** ERR reservados para este bloque: ERR-178 y ERR-179 (ninguno abierto todavía).

## 0. Qué es y qué no es
En P1 el ingeniero puso el módulo (memoria de lugar) y lo dejó prendido: FUNCIONA ×2 (79 y 85 de 180 contra 7 de O1). Aquí el módulo sigue siendo
del ingeniero, pero **nace apagado**: sus dos perillas son genes en 0 y sólo la selección puede subirlas. La pregunta es de CONDICIONES, no de
tiempo: en un mundo que paga la capacidad, ¿la selección por persistencia la prende desde cero, más que la deriva? No se pregunta si la selección
"inventa" la memoria (no: está escrita), ni nada sobre el muro de la pista vieja. Todo vale sólo en el mundo de P1 (oasis 1, extra 0.8, pobre 0.5,
dens 0.5, vista 20).

## 1. Hipótesis (director)
En el mundo con oasis, donde la memoria de lugar paga, la selección sube desde cero la perilla del módulo (sel) y la deriva no (neu); y el genoma
que deja la selección cruza más que el que deja la deriva.

## 2. Mecanismo mínimo y memoria nueva (`construye_perillas.py` sha `b5d1a10f6f913556`; carros `O1_LUGAR_GEN` `ecc996d2fecccc30`, `O1_LUGAR_GEN0` `89db6c8a74902fe1`)
Por anclas (11, cada una exactamente una vez) sobre el TEXTO de O1_LUGAR que arma `escalera/construye_p1.py` (`90dc1b6f848fac80`; texto `49eee6bb278ea097`).
- **Genes (2 floats por cuerpo, en [0, 1.5]; arrancan en (0, 0)):** `GW` = peso del bono de lugar en el valor del bocado (P1: 1.0); `GV` = ganancia
  del viaje: sin blanco a la vista va al sitio recordado sólo si `GV × recuerdo(bin) > 0.05` (P1: 1). Con (0, 0) el carro ES O1 bit a bit; con (1, 1)
  ES O1_LUGAR bit a bit (arnés). La memoria de lugar se sigue escribiendo siempre; los genes sólo deciden si se LEE.
- **Mutación:** UNA por nacimiento (parto o fundación), en UN gen al azar: `gen − 0.01 + N(0, 0.03)`, recortado. σ 0.03 es el de o1_evo (a priori).
  El **sesgo a la pérdida δ 0.01** se fijó antes de correr nada, por el nulo simulado (`nulo_perillas.py`, sec. 5): sin él la deriva sola deja el gen
  por encima de 0.10 en 47–82 % de los linajes y el control neutro deja de ser control. Con él la perilla sólo se sostiene si la selección la sostiene.
- **Cámara continua (dentro del pasaje):** cada refundación (el linaje se extinguió; ENMIENDA 5) copia, mutado, el genoma del cuerpo actual de OTRO
  linaje al azar. Sólo viajan los genes; la tabla y la memoria de lugar del fundador nacen vacías. Moneda: persistir (ser donante más tiempo). Sin juez.
- **Entre pasajes** (mundo nuevo: el oasis cae en otro sitio): `corre_perillas.siembra` = genes de los vivos muestreados cada 1 000 pasos en los
  últimos 5 000, sólo de linajes sin refundación en la segunda mitad del pasaje (respaldo: los de menos refundaciones). No lee R0, hijos ni cruza.
- **Neutro (`PS_LEE` 0):** misma cadena, mismas semillas, misma mutación, cámara y moneda; ningún cuerpo lee los genes (cada cuerpo ES O1, arnés).
- Azar propio (splitmix64 en Python puro): no toca el rng del mundo ni el del cuerpo; los dos carros pasan `revisa_carro`.
- **Memoria nueva:** 2 floats y un entero (profundidad) por cuerpo. `salida()` no cambia.

## 3. Diseño: brazos, pasajes, prueba
| brazo | cadena (5 pasajes de T 100 000) | prueba T 100 000 (sin mutación, sin cámara, UN genoma) |
|---|---|---|
| `sel` | genes leídos; arranca en (0, 0) | genoma MEDIANO de la siembra final de su cadena |
| `neu` | genes NO leídos (deriva pura) | genoma mediano de la siembra final de SU cadena (ahora sí leído) |
| `fab` | — | (1, 1): el valor de diseño de P1; TECHO |
| `o1` | — | (0, 0): PISO |
- **La prueba es monomórfica a propósito:** si la prueba mutara o sacara fundadores de una siembra variada sería otra ronda de selección y el neutro
  dejaría de ser neutro justo donde se lo mide.
- **Por qué 100k y no 25k:** la moneda que conservó la regla en `condiciones/moneda_muro` fue 100k con siembra de establecidos; con 25k casi nadie
  está establecido. **Por qué 5 pasajes:** el reloj (sec. 4); con 3 la profundidad mutacional neutra fue 39 en la exploración.
- n = 20 cadenas pareadas (mismas semillas de pasaje en sel y neu; misma semilla de prueba en los 4 brazos).

## 4. Los dos relojes (se miden y se reportan por separado, por brazo; son condición de VALIDEZ sobre el brazo neutro)
- **Profundidad mutacional** de una cadena = mediana, sobre su siembra final, del número de eventos de mutación (nacimientos: partos + fundaciones)
  en la ascendencia de cada genoma desde la base (0, 0) del pasaje 0. Es un conteo exacto que viaja con el genoma; no es "generaciones".
- **Refundaciones por cámara** de una cadena = número de reemplazos (linaje extinto que recibe la copia mutada de otro) sumados en sus pasajes.
  Se reporta también en rondas de reemplazo (÷ 9 linajes). Coincide con los fundadores que cuenta el juez (arnés (S)).
- Medido en la exploración (1 cadena, 3 pasajes): neutro, profundidad 16 → 29.5 → 39 (≈ 13 por pasaje) y 907 / 938 / 952 refundaciones; sel,
  10.5 → 15 → 30 y 972 / 669 / 255 (al establecerse, el linaje deja de refundar: el reloj de sel se frena cuando la perilla prende).
- **Umbrales (V7), justificados con esa exploración:** profundidad mutacional neutra ≥ **30** (3 veces la profundidad con la que el gen ya había subido
  en sel, 10.5) y refundaciones por cámara neutras ≥ **3 000** (3 veces las 972 del pasaje en que subió), cada una en ≥ 16/20 cadenas. Esperado con 5
  pasajes: ≈ 55–65 y ≈ 4 600. Van sobre el NEUTRO porque es la oportunidad que hubo si la perilla no ayudara; un NO sin ese reloj es NO SE LEE.
- No se usa Ne·s, ni como validez ni como predicción. La pendiente descriptiva del gen por evento de mutación usa la profundidad del PROPIO brazo.

## 5. Nulos (regla 15)
- **Deriva** (`nulo_perillas.py`, salida en `nulo_perillas_salida.txt`; 40 000 linajes, sólo la regla de mutación): con δ 0.01 la distribución es
  estacionaria desde ~30 eventos: media 0.03, mediana 0.011, P(gen > 0.05) = 0.22, P(> 0.10) = 0.07, P(> 0.15) = 0.024. Con δ 0: P(> 0.10) = 0.47–0.82.
- **PG:** bajo el nulo (genes sin efecto) sel y neu son intercambiables y los empates van en contra: P(sel > neu + 0.05) ≤ 0.5 por cadena, así que
  P(≥ 13/20) ≤ 0.132; con la deriva simulada, 0.15 por cadena y P(≥ 13/20) ≈ 4 × 10⁻⁷.
- **PC:** misma cota (≤ 0.132 por el pareado) y además la suma + 10; dos series independientes a 13/20: 0.017.

## 6. LA LETRA (`corre_perillas.lee_serie`; 21 casos sintéticos en el arnés (f))
**Validez (si una falla: NO SE LEE):**
- V1: 40 cadenas de 5 pasajes y 80 pruebas, 0 abortos, contabilidad física coherente.
- V2 (el mundo paga en estas semillas): `fab` > `o1` en linajes que cruzan en ≥ 16/20 (histórico de P1: 20/20 ×2).
- V3: toda corrida en el mundo de P1 escrito por el worker, con mordidas A+C dentro del oasis.
- V4: estado por worker: carro, `PERILLAS` 1; cadenas con σ 0.03, δ 0.01, cámara 1, `PS_LEE` 1 (sel) y 0 (neu); pruebas con σ 0, δ 0, cámara 0,
  `PS_LEE` 1 y todos los fundadores con EL genoma del brazo (mediano de su cadena; (1, 1); (0, 0)).
- V5 (desde cero y neutro): pasaje 0 con los 9 primeros fundadores de la base (0, 0); los demás pasajes, de la siembra; toda refundación, de la
  cámara; el neutro no viaja en ningún pasaje (viajes = 0); `o1` no viaja y `fab` sí.
- V7a y V7b: los dos relojes del neutro (sec. 4).
**Puertas (empates EN CONTRA):**
- **PG (el gen sube):** `GV` mediano de la siembra final de `sel` > el de `neu` + **0.05**, pareado por cadena, en **≥ 13/20**.
  El gen de la letra es `GV` y el margen 0.05 = `LG_MIN`: los dos se escribieron en el runner antes de cualquier corrida.
- **PC (cruza más que la deriva):** `sel` > `neu` en linajes que cruzan en **≥ 13/20** índices **y** suma(`sel`) ≥ suma(`neu`) **+ 10** (de 180).
**Veredictos:** FUNCIONA = válido y PG y PC. HAY ALGO MODESTO = válido y sólo una de las dos (con matiz: "el gen sube pero no cruza más que la
deriva" o "cruza más sin que el gen suba por la letra"). NO = válido y ninguna. EN EL UMBRAL: cualquier conteo a ±1 de 13 o la suma a ±1 de 10.
Bloque serie + réplica: si coinciden vale ése; si no, el menor; NO SE LEE manda.
**Descriptivos (no deciden):** trayectoria de `GV` y `GW` por pasaje en sel y neu; cadenas con `GV` > 0.05 por pasaje; `GW` pareado igual que PG
(control interno: lo que el mundo NO paga); sel contra `o1` y contra `fab`; establecidos; razón de pasos en el oasis; mundo A+C; los dos relojes
por brazo; gen por evento de mutación del propio brazo.

## 7. Regla de parada y vocabulario
- Réplica (semillas 7413xx / 7415xx) sólo si la serie da FUNCIONA, MODESTO o NO en el umbral; el runner lo exige, con el mismo sha.
- FUNCIONA ×2 → "en el mundo con oasis de P1, la selección por persistencia sube desde cero la perilla del viaje de la memoria de lugar, la deriva
  no, y el genoma que deja la selección cruza más que el que deja la deriva". Prohibido: "evoluciona la memoria", "inventa", "aprende a recordar",
  "la selección supera al diseñador", y toda comparación con el muro de la pista vieja. El módulo lo escribió el ingeniero; la selección prende su perilla.
- **Obligatorio (auditoría previa, H-1):** todo FUNCIONA o MODESTO se declara junto con el mundo A+C de sel frente a o1 (Q13, `desc['mundo_AC']`):
  si sel deja el mundo más pelado que o1, se dice en la misma frase que parte de la ventaja puede venir de vaciar el oasis.
- **Una prueba, no dos (auditoría previa, H-5):** con neu ≈ (0, 0), PC es casi "GV ≥ 0.1 frente a O1", que ya está dado por diseño (P1). FUNCIONA se
  lee como UNA evidencia (la selección sube la perilla hasta donde paga), no como dos independientes.
- MODESTO → se registra, no se repite. NO → "con reloj medido, la selección no prendió la perilla en el mundo que la paga": refuta la tesis del
  encargo en este montaje. NO SE LEE no tiene salida por esta letra (semillas nuevas, preregistro nuevo).

## 8. Predicciones firmadas (antes de la serie; calibradas con 1 cadena y 6 genomas fijos de 1 semilla, declarado)
Selección esperada, sin Ne·s: por diseño el módulo prendido lleva de 7 a 79–85 linajes que cruzan, de 9 a 133 establecidos (de 180), R0 real de
0.29 a 0.80 y de 110 a 28 fundadores por linaje. En la cámara la moneda es persistir: una ventaja de ese tamaño por ronda de reemplazo es grande.
| # | predicción | rango | p |
|---|---|---|---|
| Q1 | `fab` suma de linajes que cruzan; `o1` | [60, 100]; [0, 25] | 0.80 |
| Q2 | V2 (fab > o1 en ≥ 16/20) | | 0.93 |
| Q3 | PG pasa (`GV` sel > neu + 0.05 en ≥ 13/20) | esperado ≥ 16/20 | 0.75 |
| Q4 | `GV` mediano final: sel; neu | [0.10, 0.30]; ≤ 0.03 | 0.60 |
| Q5 | cadenas neu con `GV` final > 0.10 (nulo 7 %) | ≤ 3 de 20 | 0.80 |
| Q6 | suma de cruzan: sel; neu | [55, 100]; [0, 35] | 0.60 |
| Q7 | PC pasa (par ≥ 13/20 y + 10) | | 0.70 |
| Q8 | `GW` NO sube: sel > neu + 0.05 en ≤ 6/20 (el mundo no lo paga: 1 de 9 con GW 1 y GV 0) | | 0.75 |
| Q9 | cuándo sube: cadenas sel con `GV` de la siembra > 0.05 tras el pasaje 0; tras el pasaje 2 | ≥ 12/20; ≥ 16/20 | 0.60 |
| Q10 | en eventos de su propio brazo: profundidad mutacional de sel en el primer pasaje con `GV` > 0.05, mediana | ≤ 20 | 0.60 |
| Q11 | reloj neutro: profundidad mutacional mediana; refundaciones por cámara mediana | [45, 85]; [4 000, 5 200] | 0.60 |
| Q12 | V7a pasa; V7b pasa | | 0.88; 0.95 |
| Q13 | trampa 3: mundo A+C de sel < 0.9 × el de `o1` (sel pela el oasis) | | 0.60 |
| V | veredicto de la SERIE: FUNCIONA / MODESTO / NO / NO SE LEE | | 0.55 / 0.20 / 0.07 / 0.18 |

## 9. Control que puede fallar y qué lo refuta
- **Control:** `neu`. Puede ganar de dos formas: su gen deriva hacia arriba (PG cae) o su genoma final viaja por azar y cruza igual (PC cae).
- **Refuta la hipótesis:** NO con V7 cumplida. **La debilita:** MODESTO por PG sin PC (la perilla sube pero no paga en la letra del juez).
- **Si `GW` sube tanto como `GV`** (Q8 falla), la lectura "prende lo que el mundo paga" pierde su control interno y se dice.

## 10. Las cuatro trampas
- **Canal simétrico:** la cámara copia genes entre linajes; es el aparato de selección, igual en sel y en neu (mismas semillas y corrientes de
  mutación). Nadie lee ni escribe la pizarra. En la prueba no hay cámara.
- **Acierto sin balancear:** la medida es `cruza_real` del juez y el valor de un gen; no hay tasa de acierto. Todo pareado contra el neutro.
- **Mundo que se come la comida:** VISTO en la exploración: con `GV` 0.1–0.4 fijo el mundo A+C baja a 4.3–4.7 (O1 7.0; con (0, 1) 7.5). Nueve
  cuerpos en el oasis lo pelan. Se reporta mundo A+C por brazo (Q13); si sel gana pelando, se dice. No entra en la letra.
- **Sitios fijos:** el oasis se sortea por semilla y cada pasaje tiene semilla propia; el fundador nace sin memoria de lugar: los genes no pueden
  llevar el sitio, sólo la disposición a usar lo recordado.

## 11. Historia honesta (nada de esto cuenta; `../BITACORA.md`)
1. Arnés `identidad_perillas.py` → `identidad_perillas_salida.txt`: **ARNES PASA, 74/74**, antes de mirar números del mundo. Dos carros se
   reconstruyeron antes del primer número: el primero (rectificador simétrico, muta los dos genes, sin cámara) se cambió por aviso del coordinador
   (reloj corto en o1_libre / o1_evo) y por el nulo simulado. Fallas del arnés corregidas en el ARNÉS, no en el carro: el nombre del carro en los
   ids (regla 14), el juez no cuenta los 9 primeros cuerpos, y `GW` no cambia nada a T 4 000 (sí a T 12 000: actúa poco y tarde).
2. Humo 1 y 2 (741990–741998; T 5 000 y 20 000; 6 + 2 corridas en dos procesos): `main` de punta a punta, JSON y resumen escritos; NO SE LEE como
   corresponde. sel == neu exactos (ningún gen leído pasó el umbral en 5 000 pasos).
3. Exploración 1 (genoma fijo, semilla 741941, T 100k): cruzan de 9 con `GV` 0.06 / 0.1 / 0.2 / 0.4 / 1.0 = 1 / 4 / 5 / 4 / 4; con `GW` 1 y `GV` 0 = 1.
4. Exploración 2 (1 cadena, 3 pasajes de 100k, 741900–741902): sel `GV` 0.093 → 0.107 → 0.152, establecidos en el pasaje 2 → 7 → 9, cruzan
   1 → 3 → 4; neu `GV` 0.023 → 0.009 → 0.0, establecidos 2 / 2 / 1, cruzan 0. `GW`: sel 0.04 / 0 / 0.02; neu 0.04 / 0.04 / 0.09.
5. **Sesgo declarado:** tras la exploración se fijaron el número de pasajes (5) y los umbrales del reloj. El gen de la letra (`GV`) se eligió por P1 sec. 11 y
   quedó confirmado por la exploración 1 (no es ciego a ella); el margen 0.05 = LG_MIN. σ, δ, la cámara y la moneda estaban escritos antes de la
   exploración 2. La señal viene de UNA cadena. (Redacción corregida por la auditoría previa, H-4, antes del commit y de cualquier dato de serie.)
6. **Predicciones propias refutadas:** "la cámara da ~100 eventos de mutación por pasaje" (da ~13); "el umbral funcional del viaje es ~0.057" (con
   0.06 no paga; paga desde ~0.1); "un rectificador simétrico basta para el neutro" (no: el nulo sin sesgo prende la deriva).
7. **No se hizo:** el gen ε de PREGUNTA en el mundo con mudanza (opcional del encargo). Queda para otro bloque.

## 12. Instrumento, semillas, costo, comandos
- Runner `corre_perillas.py` sha `f98b98527155f029` (`--humo`, `--explora`, `--serie`, `--replica`, `--lee`, `--bloque`, `--reanuda`, pool ≤ 2). Cada
  corrida ES `corre_v143.tarea` (regla 14, arnés (a)) con `mundo_escalera.run`; la fila física es `corre_p1.fila` (congelado, `392b71186cf49b60`).
  JSON por trabajo y por pasaje (ERR-54); `--reanuda` salta lo hecho, reintenta abortos y rearma una cadena cortada a mitad (arnés (e)). Candados:
  shas fijados, veredicto previo, regla de parada, y preregistro, runner, constructor y carros commiteados sin cambios.
- **Semillas NUEVAS 741xxx** (grep 1-oct en .py/.md: no aparecen): serie pasajes 741000 + 10 i + p y pruebas 741201–741220; réplica 741300 + 10 i + p
  y 741501–741520; práctica 7419xx (usadas: 741900–741902, 741941, arnés 741950–741975, humo 741990–741998).
- **Costo medido** (con otra serie de pool 2 corriendo): pasaje sel 77–100 s, neu 68–78 s; prueba 75–108 s. Por índice ≈ 1 165 s; serie ≈ 23 300 s
  de CPU → **≈ 3.2 h con pool 2** (3.2–3.6 h con carga). **Pasa el objetivo de 3 h en ~10 %**: se eligió n = 20 con 5 pasajes y reanudación en vez
  de n = 10 o de un reloj corto. Si se lanza después de las 10:15 no termina antes de las 13:45: se retoma con `--reanuda`.
```
python experimentos/organelos/escalera/perillas/construye_perillas.py --verifica
python experimentos/organelos/escalera/perillas/identidad_perillas.py
python experimentos/organelos/escalera/perillas/corre_perillas.py --serie --pool 2 2>&1 | tee experimentos/organelos/escalera/perillas/serie_pool2.log     # coordinador
python experimentos/organelos/escalera/perillas/corre_perillas.py --serie --pool 2 --reanuda 2>&1 | tee -a experimentos/organelos/escalera/perillas/serie_pool2.log
python experimentos/organelos/escalera/perillas/corre_perillas.py --replica --pool 2    # sólo por la sec. 7
python experimentos/organelos/escalera/perillas/corre_perillas.py --lee <carpeta>
```
