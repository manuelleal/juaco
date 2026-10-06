# PREREGISTRO (SONDA, nada se declara) — ¿Qué régimen dejó la selección de perillas? (regimen, 1-oct-2026, biotecnólogo)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).
Carpeta `experimentos/organelos/escalera/regimen/`. Nada de `perillas/` ni de `escalera/` se edita: `corre_regimen.py` importa `corre_perillas.py`
(sha `f98b98527155f029`) y usa su carro `O1_LUGAR_GEN` (`ecc996d2fecccc30`). Arnés `identidad_regimen_salida.txt`: PASA 15/15 antes de cualquier número.
**Escrito DESPUÉS de la parte 1 (análisis de los JSON de la serie de perillas, sin correr) y de la exploración 1 de perillas (1 semilla,
`explora1_genomas_salida.txt`), y ANTES de la rejilla y de la mixta.** Modo ráfaga: n = 2 semillas; nada de esto decide ni se declara.

## 0. El hecho
Serie de perillas (FUNCIONA): el genoma de la selección (GW 0.011, GV 0.194) cruza 79 contra 80 del diseño (1, 1), pero deja el mundo A+C en 4.32
(diseño 7.16, O1 7.03), muerde más A/C (5420 vs 5182), menos B/D (3319 vs 3544), tiene más fundadores (411 vs 241), más nacimientos (333 vs 210),
vida de cuerpo 600 vs 1234, pasa menos tiempo en el oasis (5.2 vs 7.1) y viaja menos (457k vs 631k).

## 1. Lo que ya dicen los JSON (parte 1, `analiza_serie_salida.txt`, `analiza_balance_salida.txt`)
- **Mundo A+C es un termómetro del desbalance de mordidas, no de "comer sin selectividad".** 36 objetos; cada mordida u olvido (≈ 2 700 en 100k)
  repone uno uniforme: estacionario x = 18 (mBD − mAC + O)/O. Pearson medido-predicho 0.84 en 80 pruebas; medianas sel 4.32/4.40, fab 7.16/6.90,
  o1 7.03/7.09. sel pela porque muerde A/C **por encima** de B/D más que nadie (mAC − mBD 2040 vs fab 1665, o1 1636): es MÁS selectivo, no menos.
- **Dentro de sel (n 20), GV sí predice** (Spearman): viajes +0.83, mordidas dentro +0.82, partos +0.73, vida +0.69, nacimientos −0.60, fundadores
  −0.31, mundo A+C **+0.44** (más GV, menos pelado), cruce +0.14. **GW no predice nada** (|rho| ≤ 0.37, rango 0–0.055).
- **Con sel + neu (n 40) la relación GV → mundo A+C es −0.71**; con la exploración 1 ((0,1) → 7.47; (0,0.4) → 4.73; (0,0.2) → 4.32; (0,0.1) → 4.56;
  (0,0.06) → 6.43) la curva es en **U**: el pelado es propio de GV intermedio (0.07–0.4), no de GW 0 ((1,0) → 7.09; neu con GW 0.22 → 7.07).
- **Cuándo:** en el pasaje 0 de sel (GV sube de 0 a 0.096 DENTRO del pasaje) el mundo ya baja a 6.13 y rho(GV siembra, A+C) = −0.74; en p1 (GV 0.137)
  4.69 y de ahí plano (4.46, 4.53, 4.56). El pelado llega CON la subida del gen, no después.
- Economía: ingesta (1.6 × dentro + 0.4 × fuera) sel 5006 vs fab 5330; sel convierte 14.8 de ingesta por nacimiento, fab 25.9; sel muere 715 vs 476.

## 2. Mecanismo candidato (a probar, no probado)
GV multiplica el recuerdo: viaja sólo si GV × s[bin] > 0.05. Con GV 1 basta s > 0.05 (viaja casi siempre: ratio 7.1); con GV 0.19 hace falta s > 0.26:
viaja sólo cuando el recuerdo del oasis es fuerte; el recuerdo es (dS − v) con v la tabla de la letra, que sube cuando el cuerpo come en el oasis, así
que el recuerdo se gasta y el cuerpo sale, come A/C fuera (pobre), la tabla baja, el recuerdo vuelve a pesar, vuelve. **El "otro organismo" es un
viajero a medias**: 44 % de sus A/C dentro (fab 53 %), 572 mordidas A/C más fuera, 225 B/D menos (fuera hay 10× menos objetos que limpiar).
GW no entra: con GW ≈ 0 el bono no pesa en el bocado, pero (0,1) no pela.

## 3. Diseño (un proceso, ≤ 6 corridas y ≤ 200k pasos por proceso; regla de CPU: con ≥ 6 python ocupados no corre)
- **Rejilla** (`--rejilla --semilla A|B`): genomas fijos, monomórficos, sin mutación ni cámara, T 100k: (GW, GV) ∈ {(0,0.2), (1,0.2), (0,1), (1,1),
  (0.2,0.2), (0,0)}; semillas NUEVAS 743801 (A) y 743802 (B); 6 corridas por proceso, dos procesos en serie.
- **Mixta** (`--mixta`): siembra de DOS genomas, "selección" (0, 0.2) y "diseño" (1, 1), sin mutación ni cámara: cada fundador (los 9 primeros y cada
  refundación) toma uno al azar (50/50, azar propio del carro). Los fundadores por genoma son ≈ iguales por construcción; **la medida es la
  ocupación** (fracción de muestras de vivos cada 1 000 pasos por genoma = persistencia relativa) y los establecidos finales por genoma. Dos paridades
  = lista invertida (mismos sorteos → asignación espejo; arnés). Semillas 743811, 743812 × 2 = 4 corridas.
- Arnés: (1,1) == O1_LUGAR y (0,0) == O1 bit a bit (reutiliza `identidad_corta` de perillas); mixta [g, g] == fija g; [fab, o1] ≠ ambos (a T 6000:
  a T 1500 aún coincide con O1_LUGAR porque el módulo actúa tarde, visto y anotado); contabilidad por genoma; paridad espejo.

## 4. Predicciones (antes de la rejilla; calibradas con la serie y la exploración 1 de UNA semilla, declarado)
| # | predicción | rango | p |
|---|---|---|---|
| R1 | mundo A+C de (0,0.2) y de (0.2,0.2) en las 2 semillas | 3.6–5.2 (pelado) | 0.80 |
| R2 | (1,0.2) también pela (GW 1 no rescata): A+C | 3.6–5.4 | 0.70 |
| R3 | (0,1) NO pela: A+C | 6.3–8.0; y ≥ (1,1) − 0.5 | 0.75 |
| R4 | fundadores: (0,0.2) > (1,1) en las 2 semillas (el diseño persiste más por la moneda de la cámara) | | 0.60 |
| R5 | cruzan: todos los puntos con GV ≥ 0.2 en 2–6; (0,0) en 0–1 | | 0.80 |
| R6 | mixta: ocupación de fab (diseño) | 0.50–0.68 en 3 de 4 | 0.55 |
| R7 | mixta: mundo A+C intermedio | 4.8–6.5 | 0.65 |
| R8 | tragedia: la ocupación de sel en la mixta > 0.5 en ≥ 3/4 (sel gana compartiendo aunque persista menos solo) | | 0.25 |
- **Lectura:** R2 y R3 juntas = "el que pela es GV intermedio, no GW cero" (CONFIRMADA si ambas; PROBABLE si una; NO SE SABE si ninguna).
  R4 + R6 = "por la moneda de la selección el diseño es MEJOR o IGUAL; la selección se quedó en el primer escalón del gen (umbral del viaje) por
  reloj corto (39 eventos) y sesgo −0.01": si R4 falla (sel persiste más solo) y R8 pasa, la selección encontró un óptimo distinto; si R4 pasa y R8
  pasa, encontró un tramposo del pozo común.
- **Refuta la hipótesis del viajero a medias:** (1,0.2) con A+C > 6.3 en las dos semillas (GW rescata), o (0,1) pelado en las dos.
- **Qué puede fallar:** n = 2; con 9 linajes la varianza de fundadores es grande (exploración: (0,0.4) 183, (0,1) 470 en la misma semilla).

## 5. Las cuatro trampas
Canal simétrico: ninguna pizarra; en la mixta los genomas no se leen entre sí (cámara 0). Acierto sin balancear: medidas físicas del juez y del
mundo, no tasa de acierto. Mundo que se come la comida: ES el objeto de la sonda; se mide por el termómetro. Sitios fijos: oasis por semilla, semillas
nuevas, fundador sin memoria.

## 6. Semillas nuevas (grep 1-oct en .py/.md/.txt/.log: ningún 7438xx aparece): rejilla 743801–743802, mixta 743811–743812, humo 743890, arnés 743895.
