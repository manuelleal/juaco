# Predicciones ANTES de correr el experimento principal (5-oct-2026, escritas tras programar y antes del humo de 1 semilla)

Mundo 8×8, T=3000, comida se muda cada 300 pasos, dos cambios de REGLA (dos acciones intercambian su efecto) en t=1200 y t=2100, 10 semillas, capacidad del bloque C=32. Techo teórico de comida/paso ≈ 1/5.3 ≈ 0.19 (distancia Manhattan media en 8×8).

| # | predicción | prob. |
|---|---|---|
| P0 | Paso 0: el pan predice ≥ 0.98 de las 256 transiciones originales | 0.90 |
| P1 | (2) plan_pan tras el cambio de regla: tasa cae ≥ 50 % y NO recupera la 3ª comida en ≤ 300 pasos en ≥ 2/3 de los eventos de regla | 0.75 |
| P2 | (6) plan_pan_cel recupera la 3ª comida tras cambio de REGLA en mediana ≤ 150 pasos y en ≥ 15/20 eventos | 0.60 |
| P3 | (6) ≥ (2) en comida/paso en ≥ 8/10 semillas (pareado) | 0.80 |
| P4 | (6) ≥ 2× más barato en ops/decisión que (4) plan_pan_grad, y (4) recupera igual o más rápido que (6) tras regla | 0.70 |
| P5 | (3) Q tabular: comida/paso total ≤ (6); recupera tras SITIO más lento que (2)/(6) (mediana 3ª comida > 100 pasos) | 0.65 |
| P6 | (1) menos_visitado es el peor en comida/paso (≈ 0.03–0.06) pero el único cuya tasa no cae tras la regla | 0.80 |
| P7 | (5) bloque_solo entre (1) y (3) en comida/paso; tras SITIO recupera más lento que Q | 0.55 |
| P8 | (7) barajado < (6) en comida/paso en ≥ 8/10 semillas (el pago hace el trabajo) | 0.70 |
| P9 | (6c) costo < (6) pred en recuperación tras regla (sólo bloquear no basta para re-planear) | 0.65 |
| P10 | (8) sueño: tras el sueño quedan ≤ 5 células y el pan copia acierta ≥ 0.9 el mundo nuevo, con rotura del original (pan vs original < 0.9) | 0.55 |
| P11 | Régimen donde (6) gana a Q tabular y a la regla a mano: mundo más grande (12×12) o sitio que se muda más seguido (cada 100); en 8×8 con sitio cada 300 Q empata o gana | 0.50 |

## Revisión tras el humo de 1 semilla (declarado): el mundo cambió, las predicciones también

El humo con comida ESCONDIDA dio comida/paso 0.002–0.10 en todos los brazos y 2/7 recuperaciones de sitio hasta para el planificador: el experimento medía búsqueda a ciegas, no decisión. Se pasó a comida VISIBLE (el agente observa posición propia y de la comida), Q tabular sobre posición RELATIVA (generaliza entre sitios), regla a mano = ir hacia la comida con el mapa original + reflejo "si choqué, menos visitado", y 3 cambios de regla (t=900, 1800, 2700). Techo teórico ≈ 0.19 comida/paso. Predicciones revisadas ANTES de correr las 10 semillas:

| # | predicción revisada | prob. |
|---|---|---|
| R1 | Tras SITIO: (1), (2), (3), (4), (6), (8) recuperan la 3ª comida en ≤ 40 pasos en ≥ 90 % de los eventos (la meta es visible; es gratis) | 0.85 |
| R2 | Tras REGLA: (2) plan_pan cae a tasa ≤ 0.05 y no recupera en ≥ 20/30 eventos; (1) regla_mano cae también (≤ 0.08) pero el reflejo la salva a veces | 0.75 |
| R3 | Tras REGLA: (6) recupera la 3ª comida en mediana ≤ 60 pasos y en ≥ 24/30 eventos; (3) Q relativo recupera en mediana 60–200 | 0.60 |
| R4 | (6) > (3) Q en comida/paso total en ≥ 8/10 semillas; (6) ≥ (1) en ≥ 8/10 | 0.65 |
| R5 | (4) techo gradiente recupera tras regla igual o mejor que (6) pero a ≥ 100× ops/decisión y rompe el mundo original (pan vs original ≤ 0.6) | 0.75 |
| R6 | (7) barajado < (6) en ≥ 8/10 semillas | 0.75 |
| R7 | (6c) costo < (6) pred tras regla (bloquear no basta) | 0.65 |
| R8 | (8) sueño: ≤ 5 células al final y pan vs mundo actual ≥ 0.9, pan vs original < 0.8 | 0.55 |
| R9 | (5) bloque_solo < (3) Q en todo | 0.70 |
| R10 | Régimen de (6) contra Q: gana más claro con regla REGIONAL (mitad izquierda) y con sitio cada 100; Q lo alcanza o supera con cambios de regla poco frecuentes y mucho tiempo | 0.50 |

Criterio de abandono (del documento JEPA_para_Alejo, exp. B): si (6) no supera a (2) y a (5) por separado en ≥ 13/20 → "el bloque no aporta como decisor sobre un modelo del mundo". Aquí con 10 semillas: ≥ 7/10.
