# PREREGISTRO (EXPLORATORIO) — BLOQUES2: el kit grande (Opus M, 28-sep-2026, noche)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas). Pregunta del director: "¿y si le damos más cosas?". Base: BLOQUES = FUNCIONA ×2 (3c67774). EXPLORATORIO.
Escrito ANTES del humo y de la exploración, con el arnés corriendo.

## 1. Hipótesis
Con más piezas (sentidos de reserva, memoria por letra, vecino, tiempo desde el parto; acciones hacia el vecino y ventana de parto) la
selección arma MÁS órganos distintos (de patas, de parto o sociales, además del rechazo) y K sube sobre BLOQ_V.

## 2. Mecanismo (`construye_bloques2.py` → `motor_bloques2.py`, 17 anclas desde `motor_bloques.py` ff782697e54585a5)
- kit 2: sentidos 0–12, acciones 0–5 (ver docstring de `construye_bloques2.py`); tope 16 reglas (kit 1: 12, el de BLOQUES).
- Memoria nueva por cuerpo, sólo la leen las reglas: R recordada por letra (4), "mordí en mi último turno" (1), t del último parto (1),
  sesgo de ventana (1).
- Mismos operadores y tasas que BLOQUES (mutar, duplicar, borrar, insertar, HGT); la regla al azar sortea sobre el kit del brazo.
- **Kit 1 en motor_bloques2 == motor_bloques bit a bit** (arnés A): BLOQ_V es la referencia exacta de la serie.
- Costo: los sentidos del vecino recorren los cuerpos vivos (O(n)) sólo si el cuerpo tiene una regla que los usa.

## 3. Brazos y medida
ECO w90, FABRICA_ECO, vivero finito t_corte 100 000, T 500 000 (el de la serie). BLOQ_V (kit 1) · BLOQ2_V (kit 2, heredable) ·
BLOQ2_AZA_V (kit 2, sin herencia). Semillas NUEVAS 48701–48708 (grep del 28-sep: 487xx libre salvo 48759); arnés 48791–48794; humo 48795.
Medidas: persiste; K en [T/2, T]; órganos = formas de regla (sentido(parámetro) comparador → acción signo) presentes en ≥ 50 % de los vivos
en T; "activo" = umbral alcanzable y |w| mediano ≥ 0.3; familias: boca, patas, parto, social (acción vecino).

## 4. Predicciones (antes de números)
| # | cantidad | predicción | p |
|---|---|---|---|
| Q1 | BLOQ2_V persiste | ≥ 7/8 | 0.75 |
| Q2 | K(BLOQ2_V) > K(BLOQ_V) pareado | ≥ 5/8 | 0.35 |
| Q3 | órganos activos por semilla (mediana) BLOQ2_V ≥ BLOQ_V + 1 | — | 0.50 |
| Q4 | rechazo por la retina fijado en BLOQ2_V | ≥ 5/8 | 0.60 |
| Q5 | "no muerdas lo que recuerdas malo" (memF → boca −) fijado | ≥ 2/8 | 0.40 |
| Q6 | un órgano de parto activo fijado en BLOQ2_V | ≥ 3/8 | 0.50 |
| Q7 | un órgano social (acción vecino) activo fijado | ≥ 2/8 | 0.25 |
| Q8 | BLOQ2_AZA_V persiste | ≤ 2/8 | 0.80 |

## 5. Control y qué refuta
BLOQ2_AZA_V (mismo kit, sin herencia): lo fijado en BLOQ2_V que también aparece allí es deriva. "Más piezas, más órganos" cae si Q3 cae;
"más piezas, más K" cae si Q2 cae. Trampas: (1) BLOQ2_V y BLOQ2_AZA_V difieren sólo en el donante; (2) conteos pareados; (3) sin subsidio
tras t_corte; (4) letras de significado fijo: instinto, no aprendizaje (salvo memF/memL, que leen la memoria de la vida).

## 6. Números (ver 6b; 6a es la enmienda escrita antes del vivero largo)

### 6a. Enmienda de las 20:57 (DESPUÉS de ver `datos/k2`, ANTES de correr el vivero largo)
Visto: con el kit grande el linaje persiste MENOS (BLOQ2_V 4/8 vs BLOQ_V 6/8) y K cae (mediana 5.15 vs 36.20; 1/8 por encima). El rechazo por
la retina aparece en 2/8 (BLOQ_V 6/8). **Hipótesis de dilución:** el órgano de rechazo necesita sentido 3 y acción boca; en el kit 1 una regla
al azar lo es con p = 1/6 × 1/4, en el kit 2 con p = 1/13 × 1/6 (3.25 veces menos), y el vivero da una ventana FIJA (100 000) para
encontrarlo. Prueba que puede fallar: vivero largo, t_corte 250 000, T 500 000 (K en [250 000, 500 000], sin subsidio), 48701–48708:
BLOQ_VL (kit 1) y BLOQ2_VL (kit 2).
| # | predicción | p |
|---|---|---|
| L1 | BLOQ2_VL persiste ≥ 6/8 | 0.60 |
| L2 | rechazo por la retina fijado en BLOQ2_VL ≥ 5/8 | 0.55 |
| L3 | K(BLOQ2_VL) ≥ K(BLOQ_VL) − 3 en ≥ 5/8 (la diferencia se cierra) | 0.45 |
Si L1–L3 caen, no es sólo dilución: el kit grande estorba de otro modo (reglas nocivas que viajan con las buenas).

### 6b. Números y lectura (21:05; EXPLORATORIO, 8 semillas, T 500 000)
Arnés `identidad_bloques2_salida.txt` **18/18**. Humo 48795 (T 200 000): BLOQ2_V y BLOQ2_AZA_V se extinguen (`humo2_salida.txt`, JSON en `datos/humo2`).

| brazo | t_corte | persiste | K mediana (rango) | rechazo retina fijado | órganos activos/semilla (mediana) |
|---|---|---|---|---|---|
| BLOQ_V (kit 1) | 100k | 6/8 | 36.20 (0–36.7) | 6/8 | 3 |
| BLOQ2_V (kit 2) | 100k | 4/8 | 5.15 (0–36.7) | 2/8 | 2 |
| BLOQ2_AZA_V | 100k | 1/8 | 0.00 | 0/8 | – |
| BLOQ_VL (kit 1) | 250k | 8/8 | 36.73 (35.3–37.5) | 8/8 | 3.5 |
| BLOQ2_VL (kit 2) | 250k | 8/8 | 36.70 (10.5–37.9) | 5/8 | 2 |
- K BLOQ2_V − BLOQ_V: 1/8 > 0, mediana −14.58. K BLOQ2_VL − BLOQ_VL: 3/8 > 0, mediana −0.41; en 5/8 la diferencia es ≥ −3.
- **Predicciones refutadas:** Q1 (4/8), Q2 (1/8), Q3 (2 vs 3), Q4 (2/8), Q5 (1/8 con vivero 100k), Q6 (1/8), Q7 (1/8). Aciertan Q8 (1/8) y L1 (8/8),
  L2 (5/8, justo), L3 (5/8).
- **Lectura:** más piezas NO dio más K ni más órganos. Con la ventana de vivero de la serie (100k) dio MENOS: la dilución (el rechazo es 3.25× más raro al
  azar) explica la mayor parte, porque con 250k la diferencia se cierra en 5/8. En las otras 3/8 el kit grande se quedó con un órgano PEOR que tapa al mejor.
- **Órganos que aparecieron (en palabras):**
  1. rechazo por la retina (boca): en todos los brazos que persisten;
  2. **memoria** (sólo kit 2; 48707 en k2; 48701, 48702 y 48708 en k2L): "no muerdas lo que recuerdas que te hizo daño" (memF < θ → boca −). Aprende en
     vida con la primera mordida; rinde K 10–15, menos que el instinto (cada cuerpo paga una mordida de veneno por letra);
  3. **social** (sólo kit 2): "si el vecino no mordió, no muerdas" (48702 k2, K 12.9: come cuando el otro come); "aléjate del vecino" (48701 k2L, 67 %);
     "si el vecino mordió, pare antes" (48707 k2L, 56 %);
  4. forrajeo (kit 1 y 2): "ve hacia lo que tiene el píxel 1" (comida y agua; 48701 k2, 48703 y 48707 k2L);
  5. parto condicionado: "con sed / tras una mordida buena, pare antes" (parir+ o ventana+) en 4/8 del vivero largo.
- **Cautela de instrumento:** con 1–2 linajes vivos por semilla, "fijado en ≥ 50 % de los vivos" incluye reglas que viajan con el ancestro (autostop). Sólo
  el rechazo es convergente entre semillas; los demás son descriptivos. El conteo de órganos por semilla está inflado por eso y no es una medida de complejidad.
- Instrumento (sha a 16): construye_bloques2 077652af04fad845 · motor_bloques2 e365506be24bb490 · corre_bloques2 0d894a522e93766f · identidad_bloques2 67b252f74dd54663 → salida b61946b7c210d6c0.
