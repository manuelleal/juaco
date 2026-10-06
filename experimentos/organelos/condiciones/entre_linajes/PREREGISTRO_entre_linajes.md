# PREREGISTRO (EXPLORATORIO con puerta hacia serie) — SELECCIÓN SOBRE GENES EN LA CÁMARA CON COLONIZACIÓN Y SIEMBRA POR PARTOS (entre_linajes; encargo "selección real entre linajes"; 30-sep-2026, creador; escrito con el arnés PASA y ANTES del humo; con los cambios por auditoría ANTES de datos, sec. 12, ERR-158)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).
Encargo del director (30-sep), fichas del genetista y del biotecnólogo de la junta Fable. Este bloque no abre ERR (reservados ERR-158/159, sin usar).

## 0. Diagnóstico que se pone a prueba (hipótesis de la junta, no medido aún)
En los pasajes de o1_evo casi no hay selección ENTRE linajes: 9 casillas fijas; el linaje que se extingue se refunda desde la siembra del
pasaje ANTERIOR (banco de semillas; arrastre ~70 %; Ne ≈ 9), y la siembra da ~5 entradas FIJAS por linaje (5 muestras de vivos cada 1 000 pasos
en los últimos 5 000), sin importar cuántos hijos dejó. En el carro, cada fundador sortea UNA entrada uniforme de la siembra.

## 1. Hipótesis
Si (a) la siembra se reparte en proporción a los PARTOS de cada linaje y (b) el linaje que se queda sin cola se refunda con los genes de un
hijo reciente de OTRO linaje vivo de la misma pista (Moran entre linajes), la selección ve los genes de O1 a nivel de linaje y, en la pista
vieja con juez, el linaje sembrado por esa cámara (`sel`) cruza más que el de la MISMA cámara con genes que nadie lee (`neu`), con una
trayectoria direccional de al menos un gen.

## 2. Mecanismo y memoria nueva
- **Memoria nueva en el organismo: CERO.** El carro es `o1_evo/carros/O1_PAS.py` (sha `c5377ada6b28bee0`, sin tocar; 4 genes MARGEN, PRUEBA,
  PEN_OTRO, PISO; σ 0.03; perilla PS_LEE). Lo nuevo es la CÁMARA del pasaje (`camara_linajes.py`), fuera del organismo.
- **Cámara por anclas:** `pista_pob.construye_run_gen()` (sha `d4ed07b28e4ba94b`, se IMPORTA): `pista.run` (sha `9f47c65e438e0ff4`) transformado
  por 5 anclas (cada una exactamente una vez) en un generador con ganchos inicio/parto/fundador. pista.py y juez.py (`6a68f640a7832f12`) sin
  tocar. La medida del juez en cada pasaje es `corre_o1_evo.tarea` (sha `95622a2f93bb38b0`) SIN CAMBIOS: sólo se reemplaza `P.run` por la cámara
  durante el pasaje.
- **(b) Colonización:** depósito FIFO con los últimos 50 partos de la pista (índice, t, genes del hijo = `'_gen'` de `al_parir`, ya mutado);
  los partos del paso t se publican al terminar t. Cuando la pista pone un fundador limpio (ENMIENDA 5) en el linaje i, si hay entradas con
  índice ≠ i, el fundador toma los genes de una al azar (rng `[seed, i, 16, k]`; la pista usa 11–15). **Sólo los genes; la tabla de letras
  no viaja:** el colonizador nace ingenuo, como el fundador de la prueba oficial (el régimen de selección de la cámara es el de la medida).
  El colonizador cuenta como fundador. Sin candidatos (inicio del pasaje): fundador de siembra como siempre.
- **(a) Siembra ∝ partos:** mismo total que la igualada (len = 45 con 9 linajes × 5 muestras); cuotas por restos mayores (empate: índice menor)
  en proporción al contador LOCAL de partos del carro (`_TEL[i]['partos']`, sin juez); las entradas del linaje i son sus muestras de vivos en
  orden cronológico, ciclando. Con partos iguales ES la igualada (arnés g); sin partos en todo el pasaje, igualada (declarado).
  **Desalineación declarada:** los partos cuentan todo el pasaje por casilla; las muestras son de los últimos 5 000 pasos (si la casilla fue
  colonizada tarde, su peso lleva los genes del colonizador).
- **Por qué (a) y (b) juntos y no como brazos separados:** (1) presupuesto: 5 índices ≤ 2 h con pool 2 alcanza para 3 cadenas por índice
  (medido abajo: ~45 s por pasaje de 25k en un proceso); separar exigiría 2 cadenas y 2 neutros más (~2 h 50 min); (2) los dos cambios empujan
  en la MISMA dirección (subir la varianza reproductiva entre linajes); es una puerta: si la combinación no mueve nada, ninguno solo lo hará
  a este tamaño; si pasa, la serie los disecciona (brazos a-sólo y b-sólo con preregistro nuevo).
- **V143_PAS (termostato g) NO entra:** no es barato (no hay carro con la interfaz de O1_PAS: el de `reunion/opusB` usa PS_MUT y otra
  telemetría; construirlo por anclas + otros 2 brazos duplica el costo). Queda propuesto para la serie.

## 3. Brazos (índice i = 0..4; mismas semillas de pasaje en las tres cadenas: números aleatorios comunes)
| brazo | qué es |
|---|---|
| `sel` | CANDIDATO: 10 pasajes T 25 000 en la cámara con (a)+(b), PS_LEE 1 |
| `neu` | CONTROL NEUTRO: la MISMA cámara, PS_LEE 0: los genes se heredan, mutan, colonizan y se siembran ∝ partos, pero nadie los lee (arnés d: con PS_LEE 0 la física es bit a bit la de la cámara sin colonizar: la demografía no ve los genes) |
| `igual` | el pasaje de siempre (sin colonización, siembra igualada) = brazo `o1pas` de o1_evo (arnés c: bit a bit). **Se corre** con semillas nuevas en vez de reusar los JSON de o1_evo: reusar obligaría a usar las semillas 617xxx de su serie (ya vistas por el coordinador) y el costo cabe en 2 h |
| `o1` | O1 de fábrica (sólo prueba) |
**Medida OFICIAL (fuera de la cámara):** prueba T 100 000 en la PISTA VIEJA con juez (`corre_o1_evo.tarea`, fundador limpio, letra ENMIENDA 5,
PS_LEE 1), fundadores de la siembra FINAL de cada cadena (sorteo uniforme, como siempre); `o1` de fábrica. Arnés (i): la prueba del runner ES
`corre_o1_evo.trabajo('prueba')` (entrada y salida idénticas, regla 14). Medida principal: linajes que cruzan (`cruza_real`, de 9) por índice.

## 4. Instrumento, semillas, costo
- `corre_entre_linajes.py` (`--humo`, `--humo --reanuda`, `--explora --pool N ≤ 2`, `--reanuda`, `--lee`); JSON por trabajo y por pasaje;
  candados (se niega si ya hay veredicto; carpeta previa sólo con `--reanuda`; `git_limpio` de preregistro, runner, cámara y arnés); shas
  verificados en CADA worker; `E.fija` carga y verifica el carro en cada worker; identidad corta en cada corrida.
- **Semillas NUEVAS 624xxx** (grep 30-sep en todo PROYECTOS/JUACO: no aparecen en .py/.md; en .txt sólo como dígitos de decimales):
  pasaje p de la cadena i → 624000 + 10 i + p (624000–624049); prueba de i → 624201 + i (624201–624205); arnés 624950–624989; humo 624990 (pasajes),
  624998 (prueba). Reservadas para la serie (preregistro nuevo): 624300–624499 y 624501–624520.
- Costo estimado: 15 cadenas × ~450 s + 20 pruebas × ~150–175 s ≈ 2.7 h de CPU → **~1 h 25 min con pool 2** (se corrige con el humo, sec. 11).

## 5. Medidas descriptivas (no deciden)
Colonos/fundadores por pasaje (arrastre), **Ne de pesos de siembra** (1/Σw² de las cuotas por linaje; igualada = 9; no es un Ne genético) [ERR-158 H-5], partos por pasaje, trayectoria de cada gen (mediana de las
cadenas de la media de la siembra) en sel, neu e igual, desplazamiento final vs fábrica por cadena, fundadores por linaje, establecidos, R0 real,
mundo A+C, genes de los vivos al final de la prueba; pareados sel–o1, sel–igual, neu–igual, igual–o1.

## 6. LA LETRA (`corre_entre_linajes.lee_explora`; el arnés la prueba en casos sintéticos: 9 antes, 14 tras ERR-158)
**Validez (si una falla: NO APLICA):** V1 0 abortos, 15 cadenas y 20 pruebas, contabilidad coherente · V2 `o1` con mayoría que cruza (≥ 5/9) en
≥ 4/5 · V3 en las pruebas de sel, neu e igual todos los fundadores salen de la siembra · V4 PS_LEE 1 en cada pasaje de sel e igual y 0 en
cada pasaje de neu, σ 0.03, carro O1_PAS; PS_LEE 1 en las pruebas; `o1` es O1 · V5 el mecanismo actúa donde debe y sólo ahí: colonos > 0 en cada
cadena sel y neu, 0 en igual; siembra proporcional con cuotas desiguales en ≥ 1 pasaje de cada cadena sel y neu; igual siempre igualada.
**Puertas (empates EN CONTRA):**
- P1: `sel` > `neu` en linajes que cruzan en **≥ 4/5** índices.
- P2 (direccional): algún gen con desplazamiento (media de la siembra final − fábrica) del **mismo signo en ≥ 4/5** cadenas sel **y** mediana
  |desplazamiento| de sel > **2 ×** la de neu.
- P4 (**ERR-158 H-1**; antes sólo reportada, con ≥ 4/5): `sel` > `igual` en linajes que cruzan en **≥ 3/5** índices (empates EN CONTRA).
- FUNCIONA (abre la puerta a una serie con preregistro nuevo) = validez y P1 y P2 **y P4** (antes: validez y P1 y P2).
- HAY ALGO MODESTO = no FUNCIONA y (P1, o sel > neu en ≥ 3/5, o suma(sel) ≥ suma(neu) + 4). **Si P1 y P2 pasan sin P4: "HAY ALGO MODESTO
  (selección sobre genes, no atribuible a la cámara)"** (ERR-158 H-1; `lee_explora` devuelve ese matiz).
- NO = lo demás, es decir (ERR-158 H-4, alineado con el código): **sel > neu en ≤ 2/5 índices y suma(sel) − suma(neu) < 4**. EN EL UMBRAL: P1 con 3 o 4 victorias (se reporta).
- Reportada, NO decide: P3 sel > o1 en ≥ 4/5.

## 7. Qué se puede decir
- Vocabulario (ERR-158 H-1): se dice **"selección sobre genes en la cámara con colonización y siembra por partos"**; NO se dice "selección real entre linajes".
- FUNCIONA → "en la cámara con colonización y siembra por partos, la selección sobre genes mueve [gen]; el linaje sembrado cruza más que su
  neutro y que los pasajes de siempre" (5 índices, exploratorio; se pide serie). Sólo con FUNCIONA **y** P3 se escribe "candidata a primera
  mejora evolutiva sobre O1" (nunca "la evolución supera al diseñador" sin serie y réplica).
- MODESTO (selección sobre genes, no atribuible a la cámara) → "hay selección sobre genes (cruza más que su neutro y los genes se mueven con
  dirección), pero la cámara nueva no gana a los pasajes de siempre": no se atribuye a la colonización ni a la siembra por partos.
- MODESTO → se registra; no se repite con estas semillas. NO → "más selección sobre genes en la cámara con colonización y siembra por partos,
  a este tamaño, no mueve el cruce de O1".
- **Qué lo refuta** (ERR-158 H-4, alineado con el código; antes decía "sel ≤ neu en ≥ 2/5 y suma < +4"): **NO = sel > neu en ≤ 2/5 índices y
  suma(sel) − suma(neu) < 4**. Sin P2 (ningún gen 4/5 o |Δ| ≤ 2× neu) no hay FUNCIONA; P2 sola no refuta ni confirma (nulo ≈ 0.23, sec. 12).
  Si sel ≈ neu y ambos > igual: es el transporte/la demografía (colonos ingenuos, menos refundación), no la selección sobre genes.

## 8. Predicciones firmadas (antes del humo)
| # | predicción | rango | p |
|---|---|---|---|
| Q1 | `o1`: suma de linajes que cruzan (de 45) | [30, 40] | 0.75 |
| Q2 | `igual`: suma | [28, 40] | 0.70 |
| Q3 | `sel`: suma | [28, 42] | 0.70 |
| Q4 | `neu`: suma | [28, 40] | 0.70 |
| Q5 | colonos / fundadores de la cámara, mediana de pasajes, en sel y neu | ≥ 0.80 | 0.75 |
| Q6 | Ne de pesos de siembra (1/Σw², siembra ∝ partos), mediana de pasajes en sel [rótulo por ERR-158 H-5] | [3, 7] (igualada 9) | 0.60 |
| Q7 | P1 (sel > neu en ≥ 4/5) | | 0.15 |
| Q8 | P2 (algún gen direccional 4/5 y > 2× neu). **Sube por ERR-158 H-3** (antes 0.25): el nulo de P2 (bootstrap del auditor, neu contra neu) es ≈ 0.23 | | 0.35 |
| Q9 | P3 (sel > o1 en ≥ 4/5) | | 0.10 |
| Q10 | la deriva de neu es MAYOR que la de igual (mediana |Δ| de algún gen, neu > igual): Ne bajo también en el neutro | | 0.70 |
| Q11 | el gen que más se mueve en sel es MARGEN | | 0.35 |
| V | veredicto (fila original, letra sin P4) | FUNCIONA / MODESTO / NO / NO APLICA | 0.10 / 0.27 / 0.55 / 0.08 |
| V′ | veredicto con la letra de ERR-158 (FUNCIONA exige P4) | FUNCIONA / MODESTO / NO / NO APLICA | 0.07 / 0.30 / 0.55 / 0.08 |
p honesta de P1 bajo la nula: con P(sel > neu) ≈ 0.4 por índice (empates ~0.2 en contra), P(≥ 4/5) ≈ 0.09. Lo más probable es NO.

## 9. Las cuatro trampas
1. **Canal simétrico:** sel y neu comparten cámara, depósito, tasa de colonización (la demografía de neu es la de la cámara sin colonizar, arnés d),
   semillas y medida; sólo cambia si los genes se leen. El colonizador sólo trae genes (no la tabla): no hay canal cultural entre linajes.
2. **Acierto sin balancear:** la medida es `cruza_real` del juez, pareada por semilla de prueba contra el neutro; la siembra de la prueba tiene
   el mismo tamaño en sel, neu e igual.
3. **Mundo que se come la comida:** si sel gana comiendo más (MARGEN alto) y pela el mundo, se ve en mundo A+C y fundadores por linaje; se dice.
4. **Sitios fijos:** no hay sitios: la casilla es un índice y la posición se sortea al morir; las semillas de pasaje (6240xx) no son las de la
   prueba (6242xx). El colonizador sale de cualquier casilla ≠ i.

## 10. Declarado
- Desalineación partos/muestras (sec. 2). Colonización sólo de genes. Los primeros 9 fundadores del pasaje salen de la siembra (antes de que haya partos).
- En los pasajes, `fund_de_siembra` del juez de o1_evo cuenta también a los colonos (el carro los registró al crearse): lo que manda en la cámara
  es `camara.colonos`; en la prueba no hay colonización y V3 vale tal cual.
- Humo en dos procesos (6 + 4 corridas, ≤ 200 000 pasos cada uno), como en o1_evo.

## 11. Humo (se completa DESPUÉS de escribir todo lo anterior; nada de las secs. 0–10 cambió tras el humo)
- Preregistro que citan los dos logs del humo: sha `e3b9a58bf11627e9` (esta sección 11 se agregó después; secs. 0–10 idénticas).
  **Verificado (ERR-158 H-2):** las secs. 0–10 tal como estaban antes de la auditoría + la sec. 11 original ("(pendiente)") dan exactamente
  `e3b9a58bf11627e9`; la línea de costo de la sec. 4 ("~1 h 25 min … se corrige con el humo, sec. 11") y el "medido abajo: ~45 s por pasaje"
  de la sec. 2 YA estaban antes del humo (los 45 s salieron de dos pasajes de prueba de la cámara, T 3 000, s 624953/624954, antes del humo).
- Arnés `identidad_entre_linajes.py`: **PASA 45/45** (108 s), salida en `identidad_entre_linajes_salida.txt`.
- Humo (semillas 624990–624991 pasajes T 5 000 × 2, prueba 624998 T 20 000; `datos/humo/humo_20260930_170951/`): proceso 1 = 6 corridas
  (60 000 pasos), proceso 2 (`--reanuda`) = 4 corridas (50 000 pasos); 0 abortos; JSON por trabajo y `resumen.json` escritos; la letra corre
  de punta a punta (NO APLICA en humo, esperado: T 20k no permite `cruza_real` de O1, V2 falla). V1, V3, V4, V5 pasan: colonos por pasaje
  sel [46, 46], neu [24, 37], igual [0, 0]; Ne de la siembra sel 6.6–6.8, igual 9.
- Costo medido: pasaje 5k ≈ 20 s y prueba 20k ≈ 38 s en un proceso (≈ 2 ms/paso) → explora ≈ 15 × 10 × 50 s + 20 × 190 s ≈ 11 300 s de CPU
  → **~1 h 35 min con pool 2** (si dos workers no se estorban; con la serie de o1_evo corriendo en paralelo puede ir más lento).

## 12. Cambios por auditoría antes de datos (30-sep) — ERR-158
Auditor: LISTO CON CAMBIOS. Ningún dato de esta cámara (explora 6240xx/6242xx) se ha visto; sólo el humo (624990–624998, no cuenta).
- **H-1 (ERR-158): FUNCIONA exige además P4 suavizado** — `sel` > `igual` en ≥ 3/5 índices, empates en contra. Si P1 y P2 pasan sin P4, el
  veredicto es "HAY ALGO MODESTO (selección sobre genes, no atribuible a la cámara)". **Declarado: el auditor vio datos PARCIALES de la serie
  o1_evo en curso (o1pas se desplaza más que o1neu) y por eso se endurece la letra**: si los pasajes de siempre ya producen selección sobre
  genes, P1 + P2 solas no distinguen la cámara nueva de los pasajes de o1_evo. Esos datos son de OTRO experimento; ningún dato de esta cámara se
  ha visto. Cambian la sec. 6, la sec. 7, `lee_explora` (constante `GANA_IGUAL = 3`, campo `matiz`) y el caso (j) del arnés (3 casos de H-1 y
  2 de frontera de H-4). Vocabulario: "selección sobre genes en la cámara con colonización y siembra por partos", no "selección real entre
  linajes" (título, sec. 7, docstring del runner).
- **H-2: la sec. 11 y el humo.** El auditor señaló que la línea de costo de la sec. 4 (la que remite a la sec. 11) se habría añadido tras el
  humo. **Verificado por sha que no fue así** (sec. 11): esa línea y el "medido abajo" de la sec. 2 están en la versión `e3b9a58bf11627e9` que
  citan los logs del humo. Lo ÚNICO añadido tras el humo fue la sec. 11 entera (y ahora esta sec. 12 y las marcas ERR-158). Aclaración: la
  estimación pre-humo de la sec. 4 (~1 h 25 min, con pruebas de 150–175 s tomadas del log de o1_evo) queda superada por la medida del humo
  (~1 h 35 min, sec. 11).
- **H-3: nulo de P2.** Bootstrap del auditor (neu contra neu): P(P2) ≈ 0.23 sin selección. P2 es una puerta débil por sí sola; lo que pesa
  es P1 (nula ≈ 0.09) y P4. Q8 sube de 0.25 a 0.35. La letra no cambia por H-3.
- **H-4:** "qué lo refuta" alineado con el código: NO = sel > neu en ≤ 2/5 y suma(sel) − suma(neu) < 4 (secs. 6 y 7; arnés con 2 casos de frontera).
- **H-5:** "Ne de pesos de siembra" (1/Σw² de las cuotas por linaje; no es un Ne genético) en la sec. 5, en Q6 y en la clave del descriptivo
  (`*_ne_pesos_siembra_por_pasaje`) y en el log de la cadena.
- Arnés re-corrido entero tras estos cambios: **PASA 50/50** (109 s; runner `2ce1bafee633ed7b`, cámara `e2889842021e9241`, arnés `c5078a755fc38af6`; salida en `identidad_entre_linajes_salida.txt`).
- El humo NO se repite (la maquinaria de la cámara no cambió: `camara_linajes.py` sigue en `e2889842021e9241`; cambian la letra y rótulos del
  runner). El arnés se re-corrió entero con los shas finales.
