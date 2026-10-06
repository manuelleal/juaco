# INFORME — PASO B v3 (5-oct-2026, 18:05). PERILLAS DEL MURO CON TRES BRAZOS (sel · neu · pur): APTA PARA AUDITOR CORTO Y LANZAR. Nada corrido en serie.
(v1 17:20 → `INFORME_pasoB_v1_1720.md.txt`; v2 17:50 → `INFORME_pasoB_v2_1750.md.txt`)

**VEREDICTO: CONSTRUIDO EL CONTROL DE GRADIENTE `pur` Y METIDO EN LA SERIE COMO TERCER BRAZO DECISIVO. `ARNES PASA, 50/50 (534.0s)` (`identidad_muro_perillas_salida8.txt`,
shas finales fijados). Humo de main de punta a punta con POOL 3 (ERR-42): `pasoB_pur.log`, `datos/humo/humo_serie_20261005_175426/`: 3 cadenas × 2 pasajes de 5k en paralelo
(3 trabajadores) + pruebas sel/neu/pur de 20k encoladas al terminar cada cadena, luego `--reanuda` con fab y off y la letra v3 evaluada; 0 abortos; NO SE LEE por T corto, como
corresponde. Preregistro: `PREREGISTRO_muro_perillas.md` **sec. 13 (manda sobre 10–12)**.** Falta sólo el commit (candado git: preregistro, runner, constructor, arnés, nulo, carros).

## 1. Los 6 puntos
1. **Brazo `pur`:** idéntico a sel (misma cámara, mutación, semillas pareadas, el cuerpo LEE el gen) pero el valor leído se recorta a `TOPE_PUR = 0.045` (`PS_TOPE`, parámetro del
   carro: `MARGEN leído = min(gen, tope)`; el gen heredado muta y viaja libre; se reporta el gen). Tope justificado con el mapa: por encima del arranque (0.03 → 4/18, R0 0.86)
   y por debajo de la zona que cruza (0.06 → 11–15/18, R0 0.88–0.91). Prueba monomórfica de pur leída SIN tope (descriptivo `pur_prueba_sin_tope`).
2. **Letra v3 por código (12 casos sintéticos en el arnés):** FUNCIONA = PG (a ∧ b) ∧ PC ∧ **GR** (MARGEN final de sel > pur + 0.02 pareado en ≥ 13/20). PG ∧ ¬GR →
   **TRINQUETE** ("la selección purificadora y la deriva llevan el margen a la zona funcional; no hay evidencia de gradiente"), no FUNCIONA, réplica sólo con GR a ±1.
   FUNCIONA dice "la selección sube el margen porque un margen mayor persiste más (sel > pur) y el genoma cruza más que la deriva". Tabla de frases en sec. 13.
   **Margen de GR por el nulo:** sin gradiente sel y pur son intercambiables (dos cadenas purificadoras independientes, `nulo_margen.py` (5)): P(sel > pur + m) por cadena
   = 0.502 (m 0 → P(≥ 13/20) 0.135, la moneda pareada) · 0.423 (0.01 → 0.034) · **0.349 (0.02 → 0.006)** · 0.288 (0.03 → 0.0008); |sel − pur| mediana 0.037. `MARGEN_GR = 0.02`.
3. **Arnés:** pur con tope ≥ clip (0.6) == sel bit a bit (σ 0.03, cámara, T 12 000) ✔ · pur con tope 0.045 ≠ sel (actúa) ✔ · genes de fábrica con tope 0 == O1 con MARGEN 0.0
   escrito a mano ✔ · TOPE entre arranque y zona ✔ · `genoma_ok` en toda prueba (sel, neu, pur, fab, off: leído == pedido, aborto si no) · (F) 12 casos. **50/50.**
4. **Pool 3:** `POOL_MAX = 3`; ejercitado en el humo (3 cadenas en paralelo a 16.7 s cada una; las tres pruebas encoladas; 66.4 s el primer proceso, 76.2 s el `--reanuda`).
   **Costo estimado:** por índice 15 pasajes + 5 pruebas ≈ 20 × 156 s ≈ 3 120 s; serie ≈ 62 500 s de CPU → **≈ 5.8 h con pool 3** (≈ 8.7 h con pool 2); réplica igual.
5. **Preregistro sec. 13:** diseño de tres brazos, letra v3, nulo de gradiente, sesgo declarado (pur, tope, GR y margen fijados el 5-oct tras ERR-192, antes de datos de serie),
   predicciones firmadas v3.
6. **Arnés salida8, shas, comando, predicciones:** abajo.

## 2. Predicciones firmadas v3 (sec. 13)
B1 fab [100, 150], off [15, 60] (0.75) · B2 V2 (0.85) · B3a (a) 16–20/20 (0.80) · B3b (b) 12–18/20 (0.55) · B4 sel [0.05, 0.14], neu ≤ 0.02 (0.60) · B6 cruzan sel [70, 130],
neu [10, 50] (0.55) · B7 PC (0.60) · B8 sel sin mayoría como O1, fab con ella (0.70/0.70) · B10 relojes neutros [40, 90]/[3 500, 5 500], sel y pur ±30 % (0.55) · B11 V7 en los
tres brazos (0.70/0.85) · B12 sel con B+D ≤ 5: 0 (0.90) · **B13 MARGEN final de pur [0.04, 0.10] (0.60) · B14 GR en ≥ 13/20: esperado 8–14/20 (0.40) · B15 sel > pur > neu en
cruzan (0.50)** · **V: FUNCIONA 0.22 / TRINQUETE 0.30 / CONSERVA 0.13 / MODESTO 0.10 / NO 0.05 / NO SE LEE 0.20.** Razón: entre 0.045 y ~0.08 de margen leído la ventaja real es
pequeña (R0 ~0.87 → ~0.91) frente a un trinquete que mueve ±0.04 por cadena: GR es la puerta más dura.

## 3. Shas finales · comando
`construye_muro_perillas.py` 1120f56ea5dc2c0f · `carros/O1_MURO_GEN.py` 83e7fe2a5eb9efd4 · `O1_MURO_GEN0.py` e6be23e6a74718a6 · `corre_muro_perillas.py` 0d02b739a3404c19
(tras el humo sólo se añadió la clave `otro` al pareado de genes; el del humo fue 9e79d8c19b30beba) · `identidad_muro_perillas.py` 52d951507ef64e03 · `nulo_margen.py`
33eed8b55c9d4c20 · preregistro: el que quede commiteado (el runner lo registra; en el humo c0d8a444d991fa01). `SHAS_PROPIOS` = constructor y carros de arriba.
```
python experimentos/organelos/muro_perillas/construye_muro_perillas.py --verifica && python experimentos/organelos/muro_perillas/identidad_muro_perillas.py
python experimentos/organelos/muro_perillas/corre_muro_perillas.py --serie --pool 3 2>&1 | tee experimentos/organelos/muro_perillas/serie_pool3.log
python experimentos/organelos/muro_perillas/corre_muro_perillas.py --serie --pool 3 --reanuda 2>&1 | tee -a experimentos/organelos/muro_perillas/serie_pool3.log
python experimentos/organelos/muro_perillas/corre_muro_perillas.py --replica --pool 3    # sólo por la regla de parada (FUNCIONA, MODESTO, NO en el umbral, CONSERVA con (b) a ±1, TRINQUETE con GR a ±1)
```
Salida del humo con pool 3 (`pasoB_pur.log`, resumido): cadena sel MARGEN final 0.0498 · neu 0.0070 · **pur 0.0069** (2 × 5k; el gen de pur no sube en 10k: a T corto no
dice nada) · pruebas sel R0 0.667, neu 0.0, pur 0.0, fab 0.75, off 0.0 · validez V2/V7 False (T corto) · puertas PG_a True, PG_b False, PC False, GR 1/1 · VEREDICTO HUMO: NO SE LEE.

## 4. Lo no verificado
La serie; el costo real con pool 3; que V7 alcance 30/3 000 en los tres brazos; que el trinquete real (congelación en 0, no muerte) se parezca al del nulo; el poder de GR
con n = 20 (bajo el nulo intercambiable el P90 de |sel − pur| es 0.10: si la ventaja real es < 0.03 la serie dará TRINQUETE aunque exista gradiente — declarado en B14).
