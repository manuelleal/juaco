# PREREGISTRO (EXPLORATORIO) — BLOQUES6: el mundo se invierte DENTRO de una vida (Opus M, 28-sep-2026, 22:47)

Misión: llegar a la AGI por este camino. Escrito ANTES del arnés con números y ANTES de correr.

## Qué se prueba
La predicción de mi lectura de BLOQUES5, "la selección ve vidas, no siglos". Si el mundo se invierte dentro de una vida (~10^3 pasos), olvidar le
paga al individuo, y la selección debería FIJAR λ alto. Esto puede FALLAR.

## Instrumento
- `construye_bloques6.py` → `motor_bloques6.py` (1c46de780d65ff3c), 6 anclas desde motor_bloques5 (a727e6aea0fca8da).
- inv = 2: la inversión A↔B, C↔D se hace dentro del núcleo, en cualquier periodo, al empezar el paso.
- Arnés:
  - inv 0 y 1 == motor_bloques5 bit a bit;
  - inv 2 con periodo 20 000 == inv 1 (Python) bit a bit.

## Condiciones, brazos y semillas
- Periodo de inversión 500, 2 000 y 10 000 pasos; vivero hasta 100 000; T 300 000.
- Brazos:
  - ING_SEL_C_V;
  - SEL_OLV_V (15 genes + gen de olvido del cerebro, λ inicial al azar de 1e-7 a 0.1);
  - BLOQ4_V (kit 4: reglas con olvido de reglas, reprobar y olvido del cerebro);
  - BLOQ4_AZA_V.
- Semillas NUEVAS 48631–48636 (grep: libres); arnés 48685–48688.

## Predicciones (antes de números; la curva que busco es λ fijado en función del periodo)
| # | predicción | p |
|---|---|---|
| V1 | λ fijado en SEL_OLV_V (mediana de las semillas) > 1e-3 por paso con periodo 500 | 0.55 |
| V2 | λ fijado con periodo 2 000 entre 1e-4 y 1e-2 | 0.40 |
| V3 | λ fijado con periodo 10 000 < λ con periodo 500 (la curva baja con el periodo) | 0.65 |
| V4 | λ con periodo 500 > λ fijado con periodo 100 000 en BLOQUES5 (~1e-6), por al menos dos órdenes | 0.60 |
| V5 | con periodo 500, SEL_OLV_V persiste más o vive más que ING_SEL_C_V (pareado ≥ 4/6) | 0.45 |
| V6 | con periodo 500, "reprobar" activo fijado (≥ 50 %) en ≥ 2/6 semillas de BLOQ4_V | 0.30 |
| V7 | con periodo 500, alguno de los brazos persiste ≥ 3/6 | 0.40 |
| V8 | BLOQ4_AZA_V persiste ≤ 1/6 en cada periodo | 0.80 |

## Qué lo refuta
"La selección ve vidas, no siglos" cae si con periodo 500 λ tampoco se fija alto (V1 y V4) o si no depende del periodo (V3).

## Números (22:52; `python corre_bloques6.py --lee vida`; 72 corridas, ningún aborto; arnés 10/10)

**Persistencia:** 0/72 en todo. Todos se extinguen justo al acabarse el vivero (t_ext 102 000–121 000, en los tres periodos y los cuatro brazos).
K = 0 en todos. Pareado:
- SEL_OLV_V vive más que ING_SEL_C_V: 3/6 (periodo 500), 2/6 (2 000), 2/6 (10 000).
- BLOQ4_V vive más que BLOQ4_AZA_V: 1/6, 2/6, 5/6.

**Curva de λ** (olvido del cerebro en SEL_OLV_V; el gen está en 84–100 % del banco al extinguirse):
| periodo de inversión | λ fijado por paso (mediana de 6) | memoria (1/λ) |
|---|---|---|
| 500 | 8.6e-6 | ~1.2e5 pasos |
| 2 000 | 2.1e-6 | ~5e5 |
| 10 000 | 1.1e-6 | ~9e5 |
| 100 000 (BLOQUES5, otras semillas y T) | ~1e-6 | ~1e6 |
- Semilla por semilla, λ con periodo 500 > λ con periodo 10 000 en 6/6: la curva baja con el periodo.
- Pero con periodo 500 sigue siendo ~100 veces más bajo que lo que haría falta (≥ 1e-3), y queda ~35 veces por debajo de la mediana inicial al
  azar (~3e-4): la selección lo baja en todos los periodos.
- **Confusor declarado:** con periodo 500 nacen muchos menos cuerpos (arnés: 65 contra 918 nacimientos), así que la selección que empuja λ hacia
  abajo es más DÉBIL. Un λ algo más alto con periodo 500 puede ser menos selección en contra y no selección a favor. Sin el brazo sin herencia
  del gen (no se corrió) no se separa.
- **BLOQ4_V:** ni olvido del cerebro, ni olvido de reglas, ni reprobar se fijan activos (≤ 12 % del banco en todos los periodos). Sin herencia
  llegan a 0–46 %, es decir, deriva.

**Predicciones:**
- Refutadas: V1 (8.6e-6, no > 1e-3), V2, V4 (menos de un orden de magnitud sobre 100k), V5 (3/6), V6 (0/6) y V7 (0/6).
- Aciertan: V3 (la curva baja con el periodo, 6/6 pareado; con el confusor de arriba) y V8.

**Lectura: NO.** La predicción que podía fallar, falló: con el mundo invertido dentro de una vida la selección NO fija el olvido alto, y ningún linaje
sobrevive. Queda sólo una tendencia débil (λ ≈ 8 veces mayor con periodo 500 que con 100 000) que puede ser selección más débil y no a favor. Mi
lectura "ve vidas, no siglos" no alcanza. Con cambio cada 500–10 000 pasos el mundo es imposible para todos (nadie sobrevive ni con λ alto
en los fundadores al azar), así que la selección sobre λ opera cerca de la extinción, con poca fuerza.
Instrumento (sha a 16): construye_bloques6 656c6e42d97213b5 · motor_bloques6 1c46de780d65ff3c · corre_bloques6 675a99718c0344e0 · identidad_bloques6 b7d9f52fbd26f485 →
salida f84c5e7e1b187df2 (10/10).
