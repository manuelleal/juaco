# INFORME — PASO A (5-oct-2026, 16:30; ingeniero genético). Sonda con fundador NO limpio. Nada se declara.

**VEREDICTO (sonda, 2 semillas, 17:15): LA RAMPA DE MARGEN SE SOSTIENE SIN LA LIMPIEZA REGALADA (0/0 → 0/4 → 7/8 → 7/9; fábrica 5/8) y "MARGEN SOLO CRUZA" NO
SE SOSTIENE: off+MARGEN 0.25 con fl 0 → 0/9 ×2 (R0 0.24, 54 fundadores, B+D 2: nadie limpia); todo lo que vivía de los refundadores cae a 0/18 (LIMPIA 0: 0/0;
"todo" 0.5: 0/0). ERR-191 CONFIRMADO. Desde el apagado del genetista hay VALLE de 2+ con las dos reglas (off+MARGEN+LIMPIA+PISO 2, 4; +PEN 3, 5). Lote D fl 0
repetido con etiqueta corregida y verificado (genoma leído == pedido en los 82 JSON válidos). Arnés 40/40 (`salida5`); final con shas fijados en `salida6`.**

## 1. Arnés (lo que pregunta el coordinador)
- `identidad_muro_perillas_salida4.txt`: **ARNES FALLA, 33/34**. La que falla es **(K) constantes** — PRUEBA, no instrumento: exigía `BASE == APAGADO` y hoy BASE pasó a
  ser el arranque de la serie `(ARRANQUE_MARGEN, 0.5, 0.35, 0.2, 1, 1)`. El caso NUEVO **(R) fundador NO limpio PASA**: `tarea(fl=0, fábrica) == corre_v143.tarea('O1')`
  con `FL 0` (salvo el nombre del carro en los ids), `pista.fundador_limpio 0`, `FL` restaurado a 1, y difiere de fl 1. Corregida (K) (BASE = arranque + fábrica;
  `off`/`off+` sobre APAGADO; `base+` sobre BASE) → re-corrida al final de la cadena → `identidad_muro_perillas_salida5.txt`.
- **Defecto en el lote D con fl 0 (la sospecha del coordinador es correcta; lo cacé a las 16:25 antes de leer y antes de su mensaje):** `genoma('off+…')` armaba el
  genoma sobre `BASE`, que ese día dejó de ser APAGADO; el carro LEYÓ fábrica donde se pedía apagado. Comprobado sobre los JSON (telemetría `fund_gen0` = genoma que
  leyó el primer fundador): los 12 fl 0 del lote D de 15:48–16:17 tienen `leído != pedido` (p. ej. `off+MARGEN=0.25`: leído PEN 0.35, PISO 0.2, LIMPIA 1, HUECO 1); los
  otros **70 JSON del mapa (1-oct fl 1 y PASO A fl 0 de los lotes A, A2, X, X2) tienen leído == pedido**. Los 12 están apartados en
  `datos/mapa/invalidos_etiqueta_fl0_D/` con LEEME (no borrados). **Prueba añadida que lo habría cazado:** (a) estática en el arnés (K): `genoma('off+MARGEN=0.25')`
  lleva PISO = APAGADO y MARGEN 0.25; (b) dinámica en cada corrida fija: `genoma_ok` = (genoma leído por el carro == pedido); si no, la corrida es ABORTO con el texto
  "GENOMA LEIDO != PEDIDO". El lote D fl 0 se repite con la etiqueta corregida (12 corridas, ~33 min).

## 2. Tabla (cruzan/9 en s883001, s883002 · R0 real mediano · fundadores medianos · B+D por linaje)
| genoma | fl 1 (1-oct, canónico) | fl 0 (PASO A) | predicción A |
|---|---|---|---|
| MARGEN 0 | 0, 0 · 0.00 · vida 200 | 0, 0 · 0.00 · fund 2.5 · vida ~19 900 (vive y no pare) | A2 ✔ |
| MARGEN 0.03 | 0, 4 · 0.86 | 0, 4 · 0.86 · 9/9 estab | A2 ✔ |
| MARGEN 0.06 | 3, 8 · 0.88 | **7, 8** · 0.91 | A2 ✔ |
| MARGEN 0.10 | 8, 9 · 0.94 | 7, 9 · 0.94 | A2 ✔ (16/18 ≥ 10) |
| fab 0.25 = O1 | 4, 8 · 0.92 | 5, 8 · 0.93 · mayoría 2/2 | A3 ✔ |
| "todo" 0.5 | 5, 5 · 0.93 | **0, 0** · 0.29 · 37.5 fund · mundo AC 1.3 | no predicho: sin consigna pela el mundo; con fl 1 lo sostenían los refundadores |
| LIMPIA 0 | 5, 6 · 0.95 · B+D 2 | **0, 0** · 0.24 · 51.5 fund · B+D 2 · mundo AC 0.56 | A1 ✔ (= sellada 0/180) |
| off+MARGEN 0.25 (nadie limpia) | 5, 6 · 0.96 · B+D 2 | **0, 0** · 0.24 · 54 fund · B+D 2 · sin bueno 0.50 | A1 ✔ |
| off · off+PISO · off+LIMPIA | 0,0 · 0,0 · 0,0 | 0,0 · 0,0 · 0,0 | A4 ✔ |
| off+MARGEN+LIMPIA+PISO · +PEN_OTRO | 7,7 · 7,6 | 2, 4 (0.85) · 3, 5 (0.90) | A4 ✘ a medias (6 y 8 de 18, pedía ≥ 8): con fl 0 HUECO también cuenta (fab 13/18) |
Costo medido: 38 corridas de 100k, **137–172 s cada una (mediana ~156 s)** con el PC libre; el arnés 447–485 s; humo de la cadena (20k) ~16 s; humo de la serie 8 corridas 185 s.

## 3. Regla de fundador en las series registradas del muro (archivo:línea)
- O1 18–20/20 (ronda 2, r2o1mono 9101–9120): **fundador limpio 1** — `experimentos/carrera_escuderias/juez.py:536-537` (`a.fundador_limpio = 1 if a.ronda.startswith('r2')`; la ronda 2 lo exige).
- tronco_v14_3 (v143, termo como brazo, O1 como ancla): `experimentos/tronco_v14_3/corre_v143.py:56` (`FL = 1`) y `:88` (`fundador_limpio=FL`).
- o1_evo: `experimentos/organelos/o1_evo/corre_o1_evo.py:8` y `:345` (`fundador_limpio=1`).
- termostato: `experimentos/organelos/reunion/opusB/corre_termostato.py:7` ("todo por corre_pas.tarea, que ES corre_v143.tarea") → FL 1.
- Con fundador NO limpio sólo las selladas del 22-sep: sellada_mono 5001–5020 (18/20) y sellada_sinlimpia (0/20): `juez.py:536` (por defecto 0 fuera de r2).

## 4. ERR-191 (candidato, confirmado; redactado para abrirlo)
Con `fundador_limpio = 1` cada refundación crea una instancia nueva con tabla vacía; un carro con PRUEBA muerde B y D una vez por instancia antes de morir. Los 2–4
linajes que se hunden en todo monocultivo de 9 refundan cientos de veces y retiran ~500–750 objetos malos por 100k: una limpieza que ningún gen paga. Medido: O1 sin
limpieza 11/18 (fl 1, B+D = 2 por linaje establecido) contra 0/18 (fl 0) y 0/180 (sellada); "todo" 10/18 contra 0/18. O1 de fábrica no cambia (12/18 vs 13/18).
Afecta a toda comparación limpia/no limpia con fundador limpio (r2, corre_v143, o1_evo, termostato, mapa del 1-oct). Remedio: reportar B+D y fundadores por linaje;
para preguntas sobre la limpieza, fl 0 o un fundador limpio que no pruebe letras ya mordidas por el linaje (cambio de pista, fuera de este bloque).

## 5. Decisión para el PASO B (escrita antes de la serie; `PREREGISTRO_muro_perillas.md` sec. 11)
Las dos reglas son defendibles. **Decide fl 1 (canónica)**: es la letra de O1 18–20/20, del mapa y de perillas, y la rampa de MARGEN es igual con las dos reglas, así que
la pregunta de la serie no depende de ella. **fl 0 queda como segunda serie descriptiva** (`FL_SERIE = 0`, semillas 884xxx) si la primera da FUNCIONA/MODESTO.

## 6. Shas (16:25) · comandos · lo no verificado
`construye_muro_perillas.py` 8eccbf0d38591c9f · `carros/O1_MURO_GEN.py` d9b238bd516b0aeb · `O1_MURO_GEN0.py` e98f06e75d9f682f · `corre_muro_perillas.py` c787e4341621b90a ·
`identidad_muro_perillas.py` 0b73545065a0bca8 · `nulo_margen.py` 99ef5a9c62078f0b · preregistro bdee449ec037a17f (cambian al fijar `SHAS_PROPIOS` y el arranque).
```
python experimentos/organelos/muro_perillas/corre_muro_perillas.py --mapa --lote D --fl 0 ; ... --lote D2 --fl 0 ; ... --lee
```
Humo de la cadena desde MARGEN 0 (T 20k): no se extingue pero NO muta (15 partos, R0 0, profundidad 1: nadie pare) → arranque de la serie 0.03 (72 fundadores, 73 partos, profundidad 2 en 20k). No verificado: nada del PASO A queda sin verificar; con una semilla más por genoma (n = 2) nada se declara.
