# INFORME — ORGANELOS / GRAMÁTICA (Opus A, 24-sep-2026). Misión: llegar a la AGI por este camino.

**Veredicto del trabajo: FUNCIONA como instrumento.** El experimento NO está corrido: la serie, la réplica y la fuerza bruta
confirmatoria quedan reservadas en `PREREGISTRO_gramatica.md`. Mi predicción firmada para la serie es **NO (0.65)**.

## Qué construí
- **Motor y carro por anclas.** `construye_gramatica.py` construye `motor_gramatica.py` (desde `motor_eco2` 0921ee3a50ce7f7a) y
  `carros/FAMB_GRAM_ECO.py` (desde `FAMB_ORG_ECO` 75d5f4118079ff15). No toqué ningún archivo existente.
  - El pedido decía "motor_eco3": difiere de motor_eco2 solo en GENES y no tiene `ensena`. Anclé al instrumento de v2.1 y verifiqué
    motor_eco3 == motor_eco2 con los órganos apagados.
- **La gramática** (`gramatica_def.py`). Un órgano es de 0 a 4 slots de la forma (cuándo × qué × a quién × cómo) + origen.
  - Los errores de copia son: campo p 0.05, duplicación en tándem p 0.02 y borrado p 0.02. El órgano vacío es absorbente.
  - Los fundadores nacen con un slot SILENCIOSO de campos al azar.
  - Ajustes a la lista pedida: agregué «nunca»; «magnitud alta» se contrae a `sin0`; **quité «olvidar»**, porque el arnés por pieza lo
    midió bit a bit igual a copiar en w30, donde el mundo no cambia. Espacio de un slot: 135.
- **Novedad por conducta** (`conducta.py`). Un banco fijo de 5 emisores × 3 receptores da la tabla de efecto de cada gramática,
  calculada con el código real del carro. Dos gramáticas son el mismo órgano si difieren en ≤ 0.05.
- **Otros archivos:** runner `corre_gramatica.py` (humo, fuerza bruta, confirmatoria con Pool, serie con Pool, letra); deriva del
  largo sin selección `deriva_slots.py` (pedido del coordinador); humo de costo `humo_largo.py`.
- **nube-9:** `trabajo()` atrapa `SystemExit`/`Exception`, escribe el JSON con `abortado` y marca la ventana NO EVALUABLE. Además,
  en w30 a T 120 000, `max_nac_linaje` fue 1 795, lejos de 100 000.

## Identidad y arnés: `identidad_gramatica.py` → **20/20** (`identidad_gramatica_salida.txt`)
- La pedida: con la gramática fija en `[nacer/todo/hijo/copiar]` da **bit a bit** lo mismo que motor_eco2 + FAMB_ORG_ECO con
  `ensena` prendido, en VIDA, AZAR y MUT0.
- Más: sin gramática == motor_eco2; filtra0; silencioso == apagado; el rng de la gramática no toca el mundo; checkpoint; nube-9;
  errores de copia; la letra en sintéticos; banderas; arnés por pieza.
- **Falló y lo corregí antes de mirar números:**
  - (I4) comparaba la telemetría `n10.dado`, que difiere porque el filtro está en el emisor y no en el hijo; la física era idéntica.
  - (I2) no ejercitaba la rama numérica (ERR-120); agregué (I2b).
  - El primer humo cayó en un `print` después de escribir el JSON de VIDA.

## Humo y fuerza bruta (exploratorios; números vistos, declarados en el preregistro §9)
- **Humo** 21001 (T 20 000): escribe los JSON de VIDA y AZAR. **Humo largo** de práctica 21901 (T 120 000):
  - VIDA armó sola `morir/neg/hijo/promediar` (23 % del banco al corte; no diseñado, no TOP) y se extinguió (R0 0.24).
  - FIJO:ensena persiste (R0 0.98).
- **Fuerza bruta**: 136 gramáticas fijas × semilla 21101, T 18 000, 2 232 s en un proceso (`datos/fuerza_explora_s21101_T18000/RANKING.json`).

| puesto | órgano | puntaje | nota |
|---|---|---|---|
| 1 | **ensena** | 0.79 | diseñado |
| 2 | **filtra0** | 0.71 | diseñado |
| 3 | nacer/neg/hijo/copiar | 0.69 | NO diseñado; queda a 0.003 del corte del TOP |
| … | 83 de 135 le ganan al nulo | | |
| 136 | nulo | 0.00 | último |

  - «Vecino» promedia más que «hijo»: es un bien público en monocultivo, y es un riesgo para la serie.
  - Con una semilla, la persistencia es frágil (1 a 7 cuerpos en T). El TOP lo fija la confirmatoria (21201–21203).

## Costo de la serie (Python; medido: 16 s por corrida a T 18 000; 129–308 s a T 120 000)
| bloque | Pool 3 | Pool 6 |
|---|---|---|
| fuerza bruta confirmatoria | 0.6 h | 0.3 h |
| serie | 2.0 h | 1.0 h |
| réplica | 2.0 h | 1.0 h |
| prueba del ganador (si hace falta) | 1.1 h | 0.6 h |
| **todo** | **≈ 5.8 h** | **≈ 2.9 h** |

Un gemelo numba (otro agente) lo bajaría ~×40.

## Riesgos
1. El TOP de monocultivo puede no ser seleccionable: los órganos de vecino benefician a otros linajes.
2. El ranking de la fuerza bruta es a T corto (18 000) y la serie es a T 120 000.
3. La carga de errores es de ~18 % por parto y por slot, con 1e-3 de probabilidad por parto de armar un TOP desde el silencio.
4. El banco conductual no es exhaustivo (le pasó a «olvidar»).
5. Con el TOP exploratorio solo diseñado, P3 no tendría espacio.
6. La regla «gana el último slot» en la fusión es arbitraria (declarada).
7. Las semillas 21011–21050, 21201–21203 y 21301–21320 NO se tocaron.

## Mis predicciones refutadas y lo que no verifiqué
- **Refutadas en el camino:**
  - Esperaba que los órganos de hijo dominaran la fuerza bruta en media; en monocultivo gana «vecino» en media.
  - Esperaba que la regla simétrica de P5 («moda del conjunto real+sombras») tuviera potencia: no la tuvo con 1/9 de real, y la
    cambié por la concentración ANTES de la serie.
- **No verifiqué:**
  - El TOP confirmatorio.
  - Si la guardia de nube-9 muerde a T 120 000 en alguna semilla (solo lo sé para 2 semillas de práctica).
  - Pool 6 real.
  - La prueba del ganador (no tiene código; se escribe y se arnesa solo si hay FUNCIONA).
- **Qué queda:**
  - Correr la confirmatoria, la serie y la réplica.
  - Si sale NO con P5 en pie, el siguiente peldaño natural es la ficha de Reina Roja (mundo que cambia), donde «olvidar» vuelve a vivir.
