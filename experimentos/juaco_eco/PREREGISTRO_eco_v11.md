# PREREGISTRO — JUACO-ECO v1.1: el mismo vivero y el mismo corte, con un JUEZ que distingue selección de deriva (24-sep-2026, coordinador de la nube; antes de cualquier serie de v1.1)

Misión: llegar a la AGI por este camino. Carpeta: `experimentos/juaco_eco/`. Nivel: **10 (JUACO-ECO)**. Frente 2 del plan vigente.
No es candidato a tronco. No se toca ningún congelado ni ningún archivo del PC: v1.1 son **archivos nuevos** que importan los de v1.
Escrito por el coordinador de la nube bajo la regla 12 (autonomía dentro del método). El director puede rechazarlo; el veredicto de ECO v1
(**NO EVALUABLE ×2**, bitácora de la nube §1b) queda como está y **no se recalifica**.

## 0. Instrumento (sha a 16; se fija en el commit que sube este archivo)
- Runner y juez v2: `corre_eco_v11.py` (**5655c93419511162**; el sha va también en el log y en `RESUMEN.json` de cada serie). Importa sin tocar:
  - `corre_eco.py` (47d9cee4d6462116): `eco_cfg`, `sel_genes`, `BRAZOS`, `MUNDO`, `SERIE`, `ME.genoma0`;
  - `corre_eco_rapido.py` (07bf5be9dc5d634a): cambia SOLO el motor por el gemelo;
  - `motor_eco.py` (bca3033878b59622), `motor_eco_rapido.py` (edb8a15090b0f0dd), `carros/FABRICA_ECO.py` (f1163009cb5193a2).
- Gemelo: `identidad_eco_rapido.py` **120/120** (nube, 24-sep 03:34) y ruta del Pool verificada (10 JSON idénticos al original, 09:40).
  Se re-corre antes de la serie; si no da 120/120, no hay serie.
- Arnés de v1.1: `identidad_eco_v11.py` (**a674b0f689b6d5f7**), **34/34** antes del humo (salida en `identidad_eco_v11_salida.txt`): (A) el juez v2 con flujo 7 = el juez de v1; (B) el placebo saca
  otros índices del mismo banco; (C) una corrida v1.1 con T = T_lect = la de v1 en sus 26 claves; (H) la dinámica no depende de T (T 12 000
  y T 6 000 dan lo mismo hasta la lectura); (V) cada rama de la letra; (R) banderas malas abortan (ERR-115).

## 1. Por qué v1.1 (lo que falló en v1 y está escrito antes de ver datos nuevos)
ECO v1 dio **NO EVALUABLE ×2** por su condición ERR-121 (AZAR gana el juez contra G0 en 12/20 y 15/20). Dos defectos del juez, anotados
en la bitácora como candidatos a ERR:
- **nube-4:** el umbral de P3c estaba en la mediana de la nula. Bajo neutralidad AZAR "gana" cada semilla con p ≈ 0.5, así que
  P(AZAR > 10/20) = 0.41: el NO EVALUABLE saltaba casi por azar.
- **nube-6:** el juez comparaba una colonia DIVERSA (9 entradas del banco) contra una CLONAL (9 copias de G0). Si la diversidad sola alarga
  la supervivencia, AZAR le gana a G0 sin selección.

**Dato visto antes de escribir esto (declarado):** con los JSON de v1 (19101–19140, batería 19201–19220), comparar VIDA contra AZAR
pareado por semilla da 18/20 y 15/20. Por eso la predicción de P3 abajo; el umbral NO sale de ahí: sale de la nula (binomial).

## 2. Qué cambia y qué no (un cambio de instrumento; cero cambios de mecanismo)
- **Igual que v1:** mundo (pista v2 × 10, esc 90, L 3600, quimiostato 2.7 objetos por paso, 90 fundadores FABRICA_ECO, tope 3000), los 4
  brazos (VIDA, CEREBRO, AZAR, MUT0), la mutación (p 0.05, σ 0.15), el banco (200), las 8 sombras, el vivero y el **corte en 60 000**,
  el cálculo de selección contra sombras (P2) y la persistencia **leída en 120 000** (P1, P1c, P4, H-c).
- **Juez v2 (P3):** para cada semilla de la serie, la colonia de 9 entradas al azar del banco de VIDA en el corte contra la del banco de
  AZAR **de la misma semilla**, en una batería **sellada nueva 19501–19520** (mundo esc 9, 9 fundadores, sin mutación ni reposición,
  T_b 20 000). Una semilla la gana VIDA si la mediana de supervivencia de su colonia es **estrictamente mayor** que la de AZAR.
- **Placebo del juez (validez):** en VIDA y en AZAR, una SEGUNDA muestra de 9 del MISMO banco (rng de muestreo [s, 8] en vez de [s, 7])
  corre la misma batería. Puntaje = victorias de la muestra 1 + empates/2, sobre 20. Bajo la nula exacta es Bin(20, 1/2): el juez vale si
  el puntaje queda en **[5, 15]** en los dos brazos (P(fuera) ≈ 0.012 por brazo). Si no, NO EVALUABLE.
- **Horizonte largo con el gemelo:** cada corrida sigue hasta **T = 1 000 000** (940 000 pasos tras el corte). Lo que se lee en 120 000 es
  idéntico a v1 (arnés H: la dinámica no depende de T). La persistencia en 1e6 es el **bloque L**, con su propia letra (§6b).
- G0 en la batería nueva queda como **descriptivo** (AZAR contra G0 mide diversidad + deriva: la hipótesis de nube-6). No decide.

## 3. Semillas NUEVAS (grep del 24-sep en `*.py` y `*.md`: ninguna semilla 194xx–196xx en uso)
- Serie **19401–19420**; réplica **19421–19440**; batería sellada del juez **19501–19520**.
- Práctica: **19601–19609** (humo 19601; prueba del Pool 19602–19609; el arnés usa 19603–19605).

## 4. Hipótesis
- **H (VIDA):** la selección durante el vivero produce genomas cuya colonia vive más que la de genomas que sólo derivaron (AZAR), fuera
  del vivero y en semillas selladas. Es la pregunta 2 del frente 2: *¿aparece algo que el control de mutación sin selección no produce?*
- **H-L:** con esos genomas, un linaje del bicho real (FABRICA con sus 18 perillas) persiste 940 000 pasos sin comida regalada (flujo fijo,
  ERR-104) y sin fundadores repuestos tras el corte (ERR-118). Es la pregunta 1 del frente 2.

## 5. Predicciones firmadas (coordinador de la nube, con los datos de v1 a la vista)
| cantidad | rango | probabilidad |
|---|---|---|
| VIDA persiste en 120 000 /20 | 14–19 | P1 con 0.75 |
| MUT0 persiste en 120 000 /20 | 0–2 | P1c con 0.95 |
| AZAR persiste en 120 000 /20 | 9–16 | — |
| CEREBRO persiste en 120 000 /20 | 14–19 | H-c con 0.70 |
| alpha seleccionado (+) en el banco de VIDA /20 | 17–20 | P2 con 0.90 |
| **VIDA > AZAR en el juez v2 /20 — la que puede fallar** | 13–19 | P3 con 0.60 |
| placebo del juez en [5, 15], los dos brazos | — | 0.97 |
| VIDA − AZAR en 120 000 | 1–8 | P4 con 0.10 |
| VIDA persiste en 1e6 /20 | 6–16 | L1 con 0.55 |
| AZAR persiste en 1e6 /20 | 2–10 | — |
| VIDA − AZAR en 1e6 | 0–10 | L2 con 0.35 |
| veredicto v1.1 | MODESTO 0.55 · NO 0.30 · FUNCIONA 0.08 · NO EVALUABLE 0.07 | — |

## 6. Criterio por la letra (`corre_eco_v11.veredicto` y `veredicto_L`; se imprimen al final)
### 6a. Veredicto de v1.1 (por serie)
**Predicciones** (las de v1 salvo P3; P3c desaparece: la valida el placebo)
- **P1:** VIDA persiste en 120 000 en ≥ 15/20.
- **P1c:** MUT0 persiste en 120 000 en ≤ 2/20.
- **P2:** algún gen del banco de VIDA queda fuera de sus 8 sombras con el mismo signo en ≥ 15/20.
- **P3 (juez v2):** VIDA > AZAR (pareado, estricto) en ≥ 15/20. Bajo la nula P(≥ 15) = 0.021.
- **P4:** VIDA − AZAR ≥ 8 semillas persistentes en 120 000.
- **H-c:** CEREBRO persiste en 120 000 en ≥ 15/20.

**Veredicto**
- **NO EVALUABLE** si: la serie está incompleta; hay bloqueados > 0; MUT0 persiste en ≥ 10/20; AZAR da > 8/20 en algún gen; **el placebo
  del juez sale de [5, 15] en VIDA o en AZAR**.
- **FUNCIONA:** P1 + P1c + P2 + P3 + P4.
- **HAY ALGO MODESTO:** P2 + P3.
- **NO:** cualquier otro caso.

### 6b. Bloque L (por serie; mismas corridas, persistencia en T = 1e6)
- **L1:** VIDA persiste en 1e6 en ≥ 10/20. **L1c:** MUT0 en ≤ 2/20. **L2:** VIDA − AZAR ≥ 6.
- **NO EVALUABLE** si la serie está incompleta, T ≠ 1e6 o hay bloqueados.
- **PERSISTE LARGO Y LA SELECCIÓN SUMA:** L1 + L1c + L2. **PERSISTE LARGO:** L1 + L1c. **NO PERSISTE LARGO:** otro caso.

Cada bloque se declara sólo si **serie y réplica dan el mismo veredicto**; si no, vale el menor.

### Vocabulario
- Permitido: «linaje», «cuerpos vivos del brazo (N = …)», «genoma», «seleccionado contra sombras», «la colonia del banco de VIDA vive más
  que la de AZAR».
- Prohibido: «población» sin la medida al lado; «evoluciona», «especie», «vida artificial abierta», «novedad abierta». El espacio sigue
  siendo de 18 perillas: lo que v1.1 puede mostrar es adaptación heredable replicable en un espacio acotado.

## 7. Qué refuta
- **H:** P3 cae con el placebo válido (la colonia seleccionada no vive más que la derivada), o P2 cae.
- **H-L:** L1 cae (ningún linaje del bicho real se sostiene 940 000 pasos en ≥ 10/20).
- **El instrumento:** placebo fuera de [5, 15] → el juez v2 tampoco distingue; se anota como ERR y se rediseña antes de otra serie.

## 8. Puntos
Los de `PREREGISTRO_eco.md` §9, sin cambios. Los decide el director; la nube no declara porcentajes.

## 9. Costo
Gemelo: ~15–30 s por corrida de 1e6 con su juez (ECO largo, 09:45). Serie = 80 corridas + placebo + G0: ~20–40 min de pared con Pool 3.

## 10. Humo y prueba del Pool (24-sep, 10:25 UTC; números sin valor)
- Humo `--humo` (19601, VIDA y AZAR, T 30 000, corte 8 000, lectura 12 000, juez 3 semillas T_b 6 000): **3.8 s**; escribe el JSON en
  `datos/humo/eco_v11_humo_s19601_20260924_102508.json`; la letra corre y dice NO EVALUABLE (serie incompleta), como debe.
- Prueba del Pool `--prueba_pool --desde 19602 --n 2 --pool 2`: 8 corridas + G0 en 3.6 s; `RESUMEN.json` escrito.
- **Enmiendas tras el humo: ninguna.** El runner y el arnés quedan congelados hasta la réplica con los sha de §0.
