# NOTAS lote4 (auditor ciego)

Resultado: 6 copias con defecto (c03, c04, c26, c31, c36, c50), 4 limpias (c18, c23, c40, c43).

## Tiempo aproximado por copia (lectura + recomputo desde JSON)
- c03: ~20 min (la mas grande: letra v4, umbrales, runner, arnes, potencia; recalcule LI de las 3 puertas desde los crudos).
- c04: ~12 min. c18: ~12 min. c23: ~12 min. c26: ~15 min. c31: ~10 min. c36: ~10 min. c40: ~10 min. c43: ~10 min. c50: ~8 min.

## Que fue facil y que fue dificil
- Los defectos de instrumento (c36 `or` en vez de `and`, c50 `>30` en vez de `>=30`) solo se ven comparando el runner con el JSON: el log y el VEREDICTO son coherentes entre si y con el JSON, y no con el codigo. Recalcule la cantidad desde el JSON con ambas variantes.
- Los shas citados en logs/VEREDICTO coinciden con los archivos incluso en c36 y c50 (donde el runner no reproduce el log). No sirven como prueba de integridad en esta copia; no los use como argumento de limpieza.
- Los defectos de criterio (c26 R3 10/20 vs 14; c31 regla de cierre sin M2) solo aparecen cruzando preregistro con el runner, no leyendo cada uno por separado.
- Los dos hallazgos de lectura (c03, c04) son los de menor confianza: son cifras del VEREDICTO que no coinciden con el JSON, pero pueden ser descuidos del autor original y no un defecto sembrado (c03: LI de TRONCO_B citado como de PEOR, filas contiguas con los mismos rev; c04: "3 semillas" vs 4).

## Que no pude verificar sin correr la serie / sin los archivos ausentes
- c03: `no_inferior`, `med`, `a12` viven en `corre_criterio_v3.py` (ausente); confie en que el EE es sd/sqrt(n) pareado por indice (lo recalcule y reproduce el log). Los commits, `identidad_criterio_v3` 54/54 y el organismo no estan.
- c04: la lista de "diagnostico post-hoc" (error mediano 0.02/0.02/0.11/0.16) no la pude reproducir con definiciones obvias (a 60k obtengo 0.021, 0.021, +5 estimulos 0.118, +10 estimulos 0.157); no lo marque como defecto por ambiguedad de definicion.
- c18: no esta el arnes de identidad (42/42), ni `bateria.py` / `bateria_v7b.py`; los criterios de E2I/E2J/E2K del runner estan copiados a mano, no importados, y no pude compararlos con la bateria. El P5 (capacidad, adenda) esta preregistrado pero ni el runner ni el VEREDICTO lo reportan: lo anoto como completitud pendiente, no como defecto.
- c23: no estan `mundo_temporal_v8`, `organismo_caph`, `parte2_capacidad` ni `coste_techo_*.json`; KT1/KK1/KK2 no son re-ejecutables. Recalcule N*, M_max y sep desde el JSON y cuadran.
- c26: "466 corridas" del VEREDICTO no cuadra con 400 (JSON) + 40 (P4) + 6 (identidad) = 446, ni con las 420+6 del preregistro; aparece igual en las dos series, por eso no lo marque. No verifique la afirmacion de "identidad 7/7 en la copia principal".
- c31: no estan v9, ni el diagnostico `sin_plast` (script de scratchpad, corr +0.87, semillas sin divisiones 4,6,10,12,17,19).
- c36: no esta v11/v10/v11m/v11g (I1/I2 no re-ejecutables); "7 divisiones frente a 28 de v9" sin fuente en la carpeta.
- c40: no esta `corre_mundo_largo.py` (T, T_NUEVO, T_INV) ni `mundo_largo.py`; no verifique T=200000 ni las cifras historicas del preregistro (490 vs 332 en Q4, 78 vs 90 celdas). El comentario final del VEREDICTO ("el sesgo extra reduce visitas") es lectura del autor sin dato de visitas en el JSON.
- c43: `examen_v8_*.json` ausente (F0b 40/40 no verificable); recalcule las tablas, F1 y Poisson.
- c50: no esta `examen_v10_*.json` ni `bateria_v10.py` (Q1 8/8 y Q2 3 divisiones en 20/20 no verificables); recalcule Q3/Q4 desde el JSON.

## Dudas
- Si c03 y c04 estan sembradas o son errores del autor original: marcarlas es la lectura literal de "cifra citada no coincide con el JSON", pero la confianza es media/baja.
- c18 y c23 las declare limpias con confianza alta basada en recomputo de los JSON; el riesgo es un defecto en un archivo ausente (arnes, bateria).
