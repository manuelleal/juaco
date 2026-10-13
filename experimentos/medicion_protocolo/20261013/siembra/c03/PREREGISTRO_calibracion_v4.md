# PREREGISTRO — bloque V4-CAL: calibración del CRITERIO DE TRONCO v4 (ERR-94)

**Escrito ANTES del humo** (22-sep-2026). Letra que se calibra: `registro/CRITERIO_TRONCO_v4.md`. Umbrales y predicciones
en `umbrales_v4.py` (ERR-31), importado por el runner. Ninguno se toca después de correr.

## 1. Hipótesis
v4 (n = 80 en el mundo vivo, margen 12.5 en T-C ii, TRONCO_B como nulo por construcción) deja pasar al tronco contra sí
mismo con P ≥ 0.95 en las dos puertas juntas, deja pasar a un candidato inerte, y tumba a un candidato conocido como malo
y a un desplazamiento exacto de −20.

## 2. Mecanismo mínimo y memoria nueva: CERO
No se toca el organismo. Se reusa `experimentos/criterio_v3/organismo_v3cal.py` (sha `148014f68cb01785`, arnés 54/54 de
A-CAL) **por import**, con las anclas verificadas por el runner al arrancar. Lo nuevo es sólo de instrumento: TRONCO_B =
la semilla `s + 100000` (sin perilla), y el juez de v4.

## 3. Instrumento y anclas
| archivo (`experimentos/criterio_v4/`) | qué |
|---|---|
| `analiza_potencia_v4.py` | cálculo de potencia sobre los crudos de A-CAL (no simula); `--meta`: potencia de la propia calibración |
| `umbrales_v4.py` | letra v4, opciones de ERR-94 con su falso rechazo, V4-1..V4-5, P-1..P-7, semillas |
| `corre_criterio_v4.py` | runner: `--humo`, `--pool N`, `--replica A-B`, `--solo TA,TC`; verifica anclas (sha) |
| `identidad_v4.py` | arnés de lo nuevo (J1–J5 identidades, K1–K5 controles que deben fallar); escribe JSON |
| `regla14_v4.py` | kwargs campo a campo contra `corre_vivo_rep2.BRAZOS` y `mini_vivo.BRAZOS` |

Anclas reusadas (sha16): `organismo_v3cal` 148014f68cb01785 · `identidad_criterio_v3` 1356458f34134c83 ·
`corre_criterio_v3` 7f93eca0e45e167b (sólo sus funciones puras `med`, `a12`, `a12_np`, `no_inferior`) ·
`corre_vivo_rep2` 10ab45355883d98d · `mini_vivo` f3e86cbe6c17e6d7 · `organismo_vivo_rep2` 96feb4918dc5d694 ·
`organismo_v142` 17528d767fcebaf6.

## 4. Diseño
Brazos (regla 14 los verifica): OFF (`placebo = 0`, semilla s) · TRONCO_B (idéntico a OFF, semilla s + 100000) · PLACEBO
(`placebo = 1`) · PEOR (`costo = costo_a = 0.0015`). T-A: `corre_vivo_rep2` VIVO y CUELLO_MIN, T = 100 000. T-C (ii):
`mini_vivo` VIVO, `invertir_vivo_en = 50 000`. **Serie 2841–2920 (n = 80)** en las dos puertas (mundos distintos; se
declara que comparten semillas). Réplica: 80 semillas nuevas que asigna el coordinador (`--replica A-B`).
**Asignadas por el coordinador el 22-sep, antes de correr: réplica 2361–2440** (hueco entre lo usado ≤ 2360 y lo reservado
desde 2441; verificado por el auditor). Se corre con Pool 5 para respetar el tope de 14 procesos con dos Pools a la vez.
Semillas verificadas libres el 22-sep con grep sobre `registro/`, `experimentos/`, `organismo/`, `datos/` y los worktrees
`bundle`, `carrera`, `fanin`: los únicos aciertos en 2841–2940 son valores que no son semillas (`2880` = tamaño en
`escala_codigo.py`; `2876`, `2937` = vida de sitio en el humo de la fase 10). 102841–102920 sólo aparecen como pasos
de tiempo en JSON viejos, nunca como semillas. Humo 2921–2922; identidad 2923; reserva 2924–2940.

## 5. Predicciones firmadas (antes del humo)
| id | qué | predicción | de dónde |
|---|---|---|---|
| **P-1** | V4-1: P(T-A y T-C ii \| nulo) por reparto | **0.965–1.000** | meta-calibración: media 0.988, p05 0.965 |
| **P-2** | T-C (ii) sola por reparto | **0.970–1.000** | 0.987–0.990 |
| **P-3** | T-A entera sola por reparto | **0.985–1.000** | 0.999 |
| **P-4** | v2 (T-A, n = 20) sobre el mismo nulo | **0.20–0.45** (sigue rechazando al tronco) | 0.337 / 0.326 en A-CAL |
| **P-5** | v3 (n = 40, las dos puertas) sobre el mismo nulo | **0.55–0.80** | 0.656–0.683 |
| **P-6** | marginales en la banda de Bonferroni | TRONCO_B **6/6**; PLACEBO **≥ 5/6** | 0.95 por construcción; la réplica de A-CAL vio 0.627 en muertes_VIVO |
| **P-7** | PEOR, Δr mediano en los dos brazos de T-A | **≤ −60** | −74.5 … −113.5 medido ×2 |
| fracción de semillas | TRONCO_B contra OFF, semilla a semilla (no es puerta): fracción con `r_B ≥ r_OFF − 10` | **0.62–0.85** en VIVO | sd(d) ≈ 16.6: P(d ≥ −10) ≈ 0.73, ± 0.05 de muestreo a n = 80 |

Probabilidad de que todo lo anterior acierte a la vez si la letra está bien: baja (siete bandas); cada una se juzga sola.

## 6. Control que puede fallar y qué refuta
- **V4-1 < 0.95** en la serie o la réplica → v4 se retira con ERR (la letra no cumple la regla 15 que la motiva).
- **V4-2 o V4-3 caen** → ver la regla de §4 de la letra (una sola caída en una sola serie: tercera serie; dos: se retira).
- **V4-4: PEOR pasa** → la letra no tiene dientes en T-A: se retira.
- **V4-5: δ = −20 pasa > 0.05** → idem.
- **P-6 falla en TRONCO_B** (algún marginal fuera de la banda con ley idéntica por construcción) → el instrumento está
  roto (semilla desplazada, cableado): no se lee nada y se busca el defecto antes de otra serie.

## 7. Las cuatro trampas
1. Canal simétrico: no hay canal. No aplica.
2. Acierto sin balancear: no hay tasas de acierto; `r`, muertes y `rev` son conteos con signo.
3. El mundo que se come la comida: `rev` depende de encontrar B en Q4 → `vis[B]`, `vis[A]` por cuarto al lado, en los
   cuatro brazos.
4. Sitios fijos: mundo vivo con reaparición al azar; celdas y splits reportados (T-F).

## 8. Mini-prueba de un proceso (humo)
`python experimentos/criterio_v4/corre_criterio_v4.py --humo`: arnés v3 (54/54) + arnés v4 + regla 14 en subprocesos;
6 corridas de T = 30 000 (180 000 pasos): T-A VIVO semilla 2921 × {OFF, TRONCO_B, PLACEBO, PEOR} y T-C (ii) semilla 2922
× {OFF, TRONCO_B}; cableado de las etapas 5–6 con crudos **sintéticos** (n = 80, cuatro brazos; no son evidencia);
estimación de duración; escribe `datos/humo/critv4_humo_<sello>.json`. Resultado en el informe del creador.

## 9. Coste y quién corre
960 corridas por serie (640 T-A + 320 T-C ii) + identidad ~3.5 min. Lo corre el coordinador:
`python experimentos/criterio_v4/corre_criterio_v4.py --pool 6` y luego `--pool 6 --replica A-B`.

## 10. Fallos pasados que esto podría repetir
ERR-3 (recalibrar tras ver datos: la justificación es el nulo, no los candidatos) · ERR-31 (umbrales en un módulo) ·
ERR-38/regla 14 · ERR-42 (humo escribe JSON) · ERR-54 (crudos a disco antes del análisis y releídos) · ERR-87 (JSON de
subproceso por prefijo + sello) · ERR-89 (una línea por puerta con su umbral) · ERR-91 (umbral sobre el nulo) · y la
lección de la réplica de v3: **una calibración cuyo propio estimador no tiene potencia** (CAL-1 con banda que empieza en
0.90, CAL-4 con 47 % de falso disparo). Aquí V4-1 se calculó con 200 series simuladas (P(cumple) 0.985).

Creador (Opus), 22-sep-2026.
