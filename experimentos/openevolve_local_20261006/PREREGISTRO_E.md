# PREREGISTRO — BRAZO E: evolucionar a HUMO más allá de donde está (local, 6-oct-2026; escrito ANTES de toda corrida de búsqueda)

Misión: llegar a la AGI por este camino; el método manda. **Evolución de programas guiada por un modelo de lenguaje sobre un juez fijo.**
Encargo del director del 6-oct: "hagámoslo evolucionar". El instrumento, el adaptador, los cambios (a)–(d), la identidad, la cordura y
las semillas de práctica son los de `PREREGISTRO_R.md` §2–§3; aquí sólo va lo propio del brazo.

## 1. Pregunta e hipótesis
HUMO (sha 69fcfcb2473f) cruza con mayoría en 19/20 y 20/20 semillas nuevas, pero (i) "mejor que O1" no replica (gana en 11 y 14 de 20;
la puerta pedía 12), (ii) deja el mundo sin nada bueno 0.24 del tiempo contra 0.04 de O1, y (iii) su pizarra SOBRA por la letra de la
disección.

**Hipótesis H-E:** partiendo de HUMO, 30 iteraciones con un puntaje que premia cruzar **con el mundo abastecido** y en **la peor de tres
semillas** producen un programa que gana a O1 con claridad en semillas selladas nuevas y baja `frac_sin_bueno_mundo` a ≤ 0.10, sin
perder el cruce. **Nula:** HUMO está en un óptimo local del bucle; el mejor al cerrar es HUMO o un vecino que no pasa las puertas.

## 2. Puntaje del brazo E (definido aquí, antes de correr; `evaluador.py` con `JUACO_OE_BRAZO=E`)
- Etapas 1 y 2: las del brazo R (la 2 exige "cría": 0 extinciones tras t 10 000 y ≥ 2 nacimientos reales, media ≥ 5/9).
- Etapa 3, por semilla:
  `bE = [0.20·persisten/9 + 0.10·min(R0 real mediano, 1) + (cruzan/9)·(0.45 + 0.25·comida)] · (1 − muertes voluntarias)`,
  con `comida = recorte(1 − frac_sin_bueno_mundo / 0.25, 0, 1)`.
- Agregado de las 3 semillas: `0.7·media(bE) + 0.3·mín(bE)`.
- Puntaje: `0.30 + 0.70·agregado − 0.02·[algún linaje escribe en la pizarra]`.

Por qué así:
- **El premio de comida va multiplicado por los linajes que cruzan.** Un cuerpo que no se reproduce deja el mundo lleno
  (`frac_sin_bueno` 0.0 en KO_BANCO): sin el producto, ese sería el atajo.
- **0.25 como fondo de escala:** HUMO (0.24) recibe casi 0 y O1 (0.04) recibe 0.84. Hay gradiente en todo el tramo que importa.
- **El mínimo de tres semillas** pide robustez, que es lo que falló en P2 (una semilla).
- **La pizarra cuesta 0.02 fijos:** equivale a ~0.4 linajes de 9 en una semilla. Si aporta más que eso, se queda; si no, la búsqueda
  gana quitándola. Es la forma de "sin la pizarra si no aporta" sin prohibirla.
- **Valores de referencia calculados con los datos ya registrados (no corridos aquí):** HUMO ≈ 0.30 + 0.70·0.67 − 0.02 ≈ 0.75;
  O1 ≈ 0.30 + 0.70·0.75 ≈ 0.82; techo 1.00. **El puntaje pone a O1 por encima de HUMO a propósito:** lo que se busca es un programa
  por encima de los dos. Riesgo declarado: que la búsqueda sólo convierta a HUMO en algo parecido a O1 (§6, P2 lo detecta).

Lo que vuelve al modelo: el mismo resumen físico por corrida (ya traía la fracción de pasos sin nada bueno) más una línea con el número
de escrituras en la pizarra. El prompt (`config_E.yaml`) cambia sólo el párrafo final de "EL OBJETIVO", que dice lo anterior en palabras.

## 3. Semillas
| uso | semillas |
|---|---|
| E, búsqueda (`random_seed` 46) | etapa 1: 281201 · etapa 2: 281211, 281212 · etapa 3: 281221, 281222, 281223 |
| práctica (tubería, no cuenta) | 281911, 281912, 281913 |
| **EXAMEN SELLADO** | el mismo del brazo R: **282001–282020** (serie) y **282021–282040** (réplica) |

## 4. Corrida
`corre_brazo.py E --desacoplado`: programa inicial `programas/HUMO.py`, 30 iteraciones, tope de 33 llamadas. Una sola corrida de
búsqueda: lo que se declara es **el programa** (examinado en 20 + 20 selladas), no que la búsqueda sea repetible.

## 5. LA LETRA (examen en 282001–282020, T 100 000, fundador no limpio; MEJOR_E, HUMO, O1, RAIZ)
Validez: la del brazo R (V1–V5).
- **P1:** M(MEJOR_E) ≥ 15/20 (sigue cruzando).
- **P2:** MEJOR_E supera a O1 en linajes que cruzan en **≥ 13 de 20** semillas (los empates no cuentan). Nulo: sin ventaja y con ~20 %
  de empates, ganar ≥ 13 de 20 tiene p ≈ 0.02. (El examen grande usó 12; con 12 el nulo pasa el 5.7 %: por eso 13. Regla 15.)
- **P3:** mediana de `frac_sin_bueno_mundo` de MEJOR_E ≤ 0.10 (HUMO 0.24; O1 0.04).
- **P4:** suma de linajes que cruzan de MEJOR_E ≥ la de HUMO en las mismas 20 semillas (no pierde lo que había).

- **FUNCIONA:** P1, P2, P3 y P4. Y réplica del examen en 282021–282040 con la misma letra; vale el menor.
- **HAY ALGO MODESTO:** P1 y (P2 o P3).
- **NO:** lo demás. **También NO si MEJOR_E es HUMO** (mismo sha): la búsqueda no movió nada, aunque HUMO pasara alguna puerta.
- Regla 12: una puerta a ±1 del umbral dispara la réplica del examen.

Descriptivo: escrituras en la pizarra de MEJOR_E (¿la quitó?); vida mediana; mordidas malas; pareado contra HUMO por semilla.

## 6. Sospechoso de trampa (primero se lee el código; `corre_examen.py` lo marca)
Lo del brazo R §7, y además, propio de este brazo:
- `frac_sin_bueno_mundo` < 0.01 con mayoría (mejor que O1 por 4 veces): puede ser un cuerpo que casi no come y cría por otra vía.
- Vida mediana > 20 000 con mayoría: "cruza" por pocos cuerpos muy largos; se mira muertes ≥ 5 por linaje (el juez ya lo exige).
- Subida de más de 0.15 de puntaje en una sola iteración respecto del padre.
- MEJOR_E gana a O1 en ≥ 18 de 20: demasiado; se lee el código antes de creerlo.

## 7. Controles que pueden fallar
- **HUMO** en el examen (punto de partida, pareado): si MEJOR_E no lo supera en suma, no hubo evolución (P4).
- **O1** (techo a mano): P2.
- **RAIZ** (suelo).
- **El puntaje de E sobre HUMO en la tubería:** HUMO debe pasar la etapa 2 nueva y puntuar en la etapa 3 entre 0.55 y 0.90 con la
  semilla de práctica. Si puntúa ≥ 0.95, el puntaje no deja sitio para mejorar y el brazo no se lanza.

## 8. Predicciones firmadas
| # | predicción | valor o rango | p |
|---|---|---|---|
| E-1 | puntaje de HUMO en la tubería (1 semilla de práctica, etapa 3) | 0.60–0.85 | 0.75 |
| E-2 | el mejor al cerrar NO es HUMO (la búsqueda mueve algo) | — | 0.75 |
| E-3 | P1 (sigue con mayoría ≥ 15/20) | M 15–20 | 0.80 |
| E-4 | P3 (mundo sin comida ≤ 0.10) | mediana 0.03–0.20 | 0.45 |
| E-5 | P2 (gana a O1 en ≥ 13/20) | gana en 8–15 | 0.25 |
| E-6 | MEJOR_E no escribe en la pizarra | — | 0.50 |
| E-7 | mejor puntaje de búsqueda | 0.80–0.92 | 0.55 |
| V | FUNCIONA / MODESTO / NO / NO SE LEE | — | 0.15 / 0.40 / 0.40 / 0.05 |

**Qué refuta H-E:** MEJOR_E = HUMO, o MEJOR_E falla P2 y P3 a la vez.

## 9. Las cuatro trampas
Las del brazo R §11. La tercera (mundo que se come la comida) es aquí la medida central (P3) y por eso el premio de comida no se da
suelto sino en proporción al cruce.

## 10. Regla de parada
30 iteraciones, 33 llamadas o el tope común de 40 USD equivalentes. Sin más rondas sin preregistro nuevo.

Firmado: creador (Claude), 6-oct-2026, antes de lanzar E.
