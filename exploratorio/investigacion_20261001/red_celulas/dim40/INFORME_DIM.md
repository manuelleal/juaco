# INFORME DIM — Células en un espacio de D dimensiones con premio regado (1-oct-2026, exploración, SIN preregistro, 8 semillas)

**NO en aprender, HAY ALGO MODESTO en la geometría del premio.** Ninguna red de células con premio regado aprendió paridad de 3 bits en 2 000 exposiciones (0.50 de mediana en todos los repartos y todas las D; el techo Adam llega a 1.00 en 100), y el interior que aprende por premio regado va PEOR que el interior congelado (0.50 vs 0.75). Lo modesto, medido: (1) la dimensión sí cambia el mundo como dijo el director: en D=1 la red es una cuerda (8.9 saltos entrada→salida, a veces sin camino) y en D=40 un mundo pequeño (1.8 saltos), y la tarea fácil (mayoría) sólo se aprende a D ≥ 2; (2) el premio regado por el grafo SÍ discrimina quién aportó (correlación premio–aporte 0.25–0.35 en D ≥ 3, 0.00 con premio global, ≈0 barajado) y deja 24–34 tramposas de 195 contra **99–150 con "todas se llevan el premio"**; pero saber quién aportó no bastó para que aprendieran.

Misión: llegar a la AGI por este camino. Carpeta `PROYECTOS\JUACO\investigacion_20261001\red_celulas\dim40\`: `dim40.py` (red, repartos, techo, medidas), `analiza.py` (tablas), `datos\barrido.json` (crudo), `datos\tablas.txt`. Nada se commiteó; informes 1–3 del colega intactos. CPU: 11 min el barrido + ≈ 5 min de humos (me pasé 1 min del tope; por eso NO corrí el barrido de radio λ ni "mover células").

## 1. Qué se construyó (una lectura)
- **Geometría en vez de capas**: N = 200 células con posición al azar en [0,1]^D; cada una OYE a sus k = 8 vecinas más cercanas (las 2 lectoras de salida oyen a 40). 3 células de entrada (bits ±1, fijadas) y 2 de salida (una por clase) viven en el mismo espacio. La señal da T = 10 pasos por el grafo (recurrente, tanh). Sin capas.
- **Premio regado**: cada salida suelta R_o = −(y_o − objetivo_o)² menos su promedio móvil; se riega hacia atrás por el grafo (de la salida a quien la alimenta) y decae λ^saltos (λ = 0.5). Cada célula recibe UN número r_i. Normalizado para que el premio medio por célula sea igual en todos los repartos.
- **Regla local de tres factores**: Δw_ij = η · r_i · Σ_t ξ_i(t)·x_j(t) (mi ruido × lo que oí = elegibilidad). Sin gradiente ni retropropagación dentro de la red. Escala sináptica local (cada célula conserva el tamaño de sus pesos). Las 2 lectoras usan su propio error (regla delta, local a ellas).
- **Tareas**: A = paridad de 3 bits (necesita células intermedias; azar 0.5), 2 000 exposiciones; luego cambio de regla B = mayoría, 2 000 más. Evaluación sin ruido cada 100.
- **Brazos** (mismas semillas 1–8): regado · global ("todas se llevan el premio") · barajado (el regado permutado) · camino (grupos chicos de 4 comparten) · aleatorio (grafo sin geometría, mismo grado) · congelado (el interior NO aprende; sólo las lectoras) · TECHO MLP 3-266-2 (1 600 parámetros ≈ N·k), Adam + entropía cruzada, mismo flujo.
- **Medidas**: acierto final, exposiciones hasta 0.9, saltos entrada→salida, células útiles (aporte contrafactual > 0.01 al silenciarlas), útiles que recibieron premio, tramposas (cobran en el cuarto superior y aporte ≈ 0), correlación premio recibido–aporte.

## 2. Tabla D × medidas (mediana [mín–máx], 8 semillas; `datos\tablas.txt` tiene todas las filas)

| D | saltos ent→sal | A paridad: regado / congelado / global | B mayoría, exp. hasta 0.9: regado / congelado / global | útiles con premio (regado) | tramposas: regado / global / barajado | corr premio–aporte: regado / global |
|---|---|---|---|---|---|---|
| 1 | 8.9 [1–∞] | 0.50 / 0.50 / 0.50 | nunca / nunca (1/8) / nunca | 32 [16–48] | 34 / **150** / 42 | 0.09 / 0.00 |
| 2 | 3.9 [1.8–6.2] | 0.50 / 0.50 / 0.50 | 700 (1/8) / **300 (5/8)** / 500 (1/8) | 38 | 28 / 146 / 40 | −0.02 / 0.00 |
| 3 | 3.5 [2.3–4.0] | 0.50 / 0.62 / 0.50 | 800 (1/8) / **500 (7/8)** / 850 (2/8) | 48 | 26 / 124 / 30 | 0.24 / 0.00 |
| 10 | 2.2 [2.0–2.7] | 0.50 / **0.75** [0.5–1.0] (2/8 a 0.9) / 0.50 | 450 (6/8) / 800 (3/8) / 1300 (6/8) | 68 | 28 / 106 / 31 | 0.25 / 0.00 |
| 40 | 1.8 [1.5–2.5] | 0.50 / **0.75** (1/8) / 0.50 | 1100 (4/8) / 1400 (5/8) / 400 (3/8) | 58 | 24 / 99 / 34 | **0.35** / 0.00 |
| aleatorio (sin geometría) | 2.1 | 0.50 | 550 (8/8) | 59 | 26 | 0.42 |
| camino (D=40 / D=2) | 1.8 / 3.9 | 0.50 / 0.50 | 1000 (5/8) / 600 (1/8) | 76 / 47 | 24 / 29 | 0.07 / 0.00 |
| **TECHO Adam** | — | **1.00 (8/8 en 100)** | **100 (8/8)** | — | — | — |

## 3. Qué reparto ganó
- **En aprender: ninguno**; el mejor "reparto" es no repartir (congelado: 0.75 en A a D ≥ 10, mayoría 7/8 a D=3). Todo premio al interior (regado, global, barajado, camino) baja A a 0.50: el interior en movimiento cambia los rasgos que las lectoras están aprendiendo y nadie converge. En B (fácil) regado y congelado empatan dentro del rango.
- **En tramposas: regado y camino (24–34) ≪ global (99–150 de 195)**. "Si hay muchas conexiones todas se llevan el premio" literal cría tramposas en masa: cobran sin aportar porque el premio no mira quién aportó (correlación 0.00). El regado sí mira (0.25–0.35) y el barajado lo destruye (≈0): la geometría dirige el premio. Pero dirigirlo no se convirtió en aprender.

## 4. Dónde le gana o pierde al techo
Pierde en todo lo que es aprender: paridad 0.50–0.75 vs 1.00 en 100 exposiciones; mayoría 300–1 400 vs 100. El techo tiene 1 600 parámetros y gradiente; aquí 1 600 pesos y un número regado. No hay costo que compense: no aprende.

## 5. ¿Importa la dimensión? Sí, y la imagen es ésta
Imagina 200 personas paradas en una fila (D=1): para avisarle algo a la del fondo el mensaje pasa de boca en boca 9 veces y a veces ni llega (hubo semillas con entradas sin camino a la salida). Pon a las mismas 200 personas en una plaza (D=2): 4 pasos. En un edificio (D=3): 3.5. En un "mundo" de 40 dimensiones todas quedan a menos de 2 pasos de todas: es una fiesta donde cada uno oye a cualquiera. Eso se midió: 8.9 → 3.9 → 3.5 → 2.2 → 1.8 saltos. Y la tarea fácil (mayoría) sólo se aprende cuando el mensaje llega (D ≥ 2); en la fila nadie la aprende. Lo que NO pasó: la hipótesis contraria "en D alto el premio se vuelve ruido" tampoco ganó (la correlación premio–aporte SUBE con D: 0.09 → 0.35), y el grafo aleatorio (que ya es mundo pequeño, 2.1 saltos) hace lo mismo que D=40. Es decir: la dimensión importa sólo porque acorta caminos; a partir de D ≈ 10 ya no suma nada que un grafo al azar no dé. El punto bueno está en "mundo pequeño" (D ≥ 3 o aleatorio), no en 40.

## 6. Las tres variantes de mecanismo probadas antes de rendirme (humos de 1 semilla, D = 2 y 40)
1. Ruido + premio regado puro (REINFORCE con tres factores): 0.50 siempre; los pesos engordan por el paseo al azar y la red se satura (pérdida 4.0 = salidas constantes).
2. Lo mismo + escala sináptica local (homeostasis): ya no se satura, sigue 0.50 con η 0.001–0.02 y σ 0.1–0.3.
3. Lectoras con regla delta propia + interior por premio regado (la versión del barrido): con σ 0.3 el ruido del interior cambia los rasgos más que la entrada misma (0.47 vs 0.45) y las lectoras no pueden leer; con σ 0.03 e interior CONGELADO aprende paridad en D=40 (1.00 en una semilla); con interior en movimiento (η ≥ 0.0003) vuelve a 0.50. Diagnóstico: los rasgos del interior están linealmente separados para paridad desde el inicio (ajuste exacto por mínimos cuadrados en D=2 y D=40); el problema es que la lectora con regla delta en línea y 8 patrones es lenta, y cualquier plasticidad del interior le mueve el piso.

## 7. Frases que el director SÍ puede decir, y las que todavía no
SÍ: (1) "Con células en un espacio, más dimensiones acortan el camino entrada→salida (9 saltos en 1D, menos de 2 en 40D) y la tarea sencilla sólo se aprende cuando el camino existe (D ≥ 2)". (2) "Un premio que se riega por el grafo y decae con la distancia sí llega a las células que aportaron (correlación 0.35) y deja 4–6 veces menos tramposas que dar el mismo premio a todas (24 vs 99–150 de 195); el barajado lo confirma". (3) "'Todas se llevan el premio' literal cría tramposas: la mitad de la red cobra sin aportar".
TODAVÍA NO: "con 40 dimensiones aprende más" (a partir de D ≈ 10 no cambia nada; un grafo al azar hace lo mismo); "el premio regado enseña" (saber quién aportó no se convirtió en aprender: 0.50 en paridad, peor que no aprender); "le gana al gradiente" (pierde 10× en exposiciones y no llega); "muchas conexiones rápidas que todas influyan" (aquí k = 8; no se barrió k).

## 8. Siguiente paso más chico
Una tarde: quedarse con lo que funcionó (interior congelado, D ≥ 3) y hacer que el premio regado NO mueva pesos sino **mueva células** (la geometría se aprende: una célula que cobra se acerca a la salida y entra al campo auditivo de la lectora; la que no cobra se aleja). Eso usa justo lo que sí se midió (el regado discrimina quién aportó) sin el problema que mató el aprendizaje (pesos del interior cambiando debajo de la lectora). Está escrito en `dim40.py` (`mueve`, `--exp mover`) pero NO corrido por el tope de CPU. Predicción que puede fallar: mover acorta "exposiciones hasta 0.9" en mayoría por debajo de 300 (congelado D=2) en ≥ 6/8 semillas; si no, se cierra.

## 9. Lo puesto a mano, cómo reproducir, lo no verificado
- A mano (viendo humos de 1 semilla, declarado): T = 10; ganancia 1.3 y entradas ×3 (sin eso la señal muere a los 3 saltos); lectoras que oyen a 40 (con 8 no leen); σ = 0.03; η = 0.0003; η lectoras 0.02; λ = 0.5; grupos de camino = 4; tope de pesos y sesgos; promedio móvil 0.95.
- Reproducir: `cd dim40; python dim40.py --exp barrido --semillas 8 --out datos; python analiza.py` (≈ 11 min en PC compartido). Humo: `python dim40.py --exp humo`.
- No verificado: barrido del radio λ (`--exp radio`) y "mover" (`--exp mover`), escritos y sin correr; N = 400 y D = 100 (`--exp grande`), sin correr; k > 8; más de 2 000 exposiciones (el congelado a D=40 seguía subiendo); otra tarea (suma mod 7); 8 semillas sin réplica; nada preregistrado; medidas de tramposa y aporte con umbrales (0.01, 0.005, cuartil superior) elegidos sin calibrar. La corrida del barrido se hizo con la versión del código ANTERIOR a vectorizar la elegibilidad (mismo cálculo, otro orden de sumas: puede diferir en el último decimal). La "corr premio–aporte" en el brazo global es 0 por construcción (premio idéntico para todas): es la cota, no una medida independiente.

## 10. Mover (añadido 14:10, encargo del coordinador): NO, se cierra
**NO.** Predicción firmada: interior congelado + células que se mueven hacia donde cobran → mayoría a 0.9 en < 300 exposiciones en ≥ 6/8 semillas. Salió **1/8 (D=3), 4/8 (D=10), 2/8 (D=40)**; el control sin movimiento dio 2/8, 6/8, 2/8 y el de movimiento al azar 1/8, 4/8, 2/8. Mover hacia el premio es PEOR que no moverse en acierto final (0.62 / 0.50 / 0.50 contra 0.94 / 1.00 / 1.00). En paridad, nadie (0.50 con movimiento; 0.62–0.75 quieto).

Diseño: brazo congelado del barrido (σ 0.03, lectoras oyen 40); cada 200 exposiciones cada célula compara su energía (premio cobrado) con la de otra al azar y, si la otra cobra más, se acerca a ella un 30 % del trecho (`rico`); control `azar` = el mismo tamaño de paso en dirección al azar; control `quieto` = sin movimiento. Se reconstruye el grafo de k vecinas conservando los pesos de las aristas que sobreviven. Mayoría sola (1 500 exposiciones) y paridad sola (2 000), D ∈ {3, 10, 40}, semillas 1–8. CPU 1.9 min. Crudo `datos\mover.json`, tabla `datos\tabla_mover.txt` (`python dim40.py --exp mover --semillas 8 --out datos; python analiza_mover.py`).

| tarea | D | modo | acierto final | exp. hasta 0.9 | semillas < 300 | saltos ent→sal al final | dist. media a la salida |
|---|---|---|---|---|---|---|---|
| mayoría | 3 | rico | 0.62 [0.50–0.75] | 300 (3/8) | 1/8 | 5.0 [1.5–∞] | **0.25** |
| mayoría | 3 | azar | 0.75 | 100 (1/8) | 1/8 | 3.9 | 0.48 |
| mayoría | 3 | quieto | **0.94** | 800 (7/8) | 2/8 | 3.5 | 0.50 |
| mayoría | 10 | rico | 0.50 | 100 (4/8) | 4/8 | **∞** [2.0–∞] | 0.75 |
| mayoría | 10 | azar | 0.88 | 100 (7/8) | 4/8 | 2.2 | 1.13 |
| mayoría | 10 | quieto | **1.00** | 100 (6/8) | **6/8** | 2.2 | 1.11 |
| mayoría | 40 | rico | 0.50 | 100 (2/8) | 2/8 | **∞** | 1.80 |
| mayoría | 40 | azar | 0.94 | 500 (7/8) | 2/8 | 2.0 | 2.53 |
| mayoría | 40 | quieto | **1.00** | 400 (5/8) | 2/8 | 1.8 | 2.48 |
| paridad | 3 / 10 / 40 | rico | 0.50 / 0.50 / 0.50 | nunca | 0/8 | 5.0 / ∞ / ∞ | — |
| paridad | 3 / 10 / 40 | azar | 0.50 / 0.50 / 0.50 | nunca / 1 / 1 de 8 | 0/8 | 4.0 / 2.3 / 2.0 | — |
| paridad | 3 / 10 / 40 | quieto | 0.62 / 0.75 / 0.75 | nunca / 2 / 1 de 8 | 0/8 | 3.5 / 2.2 / 1.8 | — |

Por qué falla, con la imagen: el premio se riega desde las salidas, así que "quien cobra" vive cerca de la salida; todas las células corren hacia allá (la distancia media a la salida baja a la mitad en D=3) y se apiñan alrededor de las lectoras. Las entradas no se mueven y se quedan solas: **nadie las oye** (saltos entrada→salida = ∞ en D=10 y 40: la señal ya no llega) y la red responde siempre lo mismo (0.50). Es "todas se van a cobrar al mismo sitio" convertido en geometría: la aglomeración rompe el camino. El movimiento al azar de la misma magnitud daña poco (0.75–0.94): el daño no es moverse, es moverse hacia el premio. Frase que SÍ puede decir el director: "si las células se mueven hacia donde se cobra, se apiñan en la salida y abandonan la entrada: el premio regado atrae, no organiza". NO: "la geometría se aprende". Lo que haría falta y no se probó (CPU): un segundo químico regado desde las ENTRADAS, o un costo por apiñarse, para que una célula quiera estar a mitad de camino; es un paso nuevo, no la continuación de éste. Semillas 1–8 sin réplica, sin preregistro; el `quieto` de esta tabla no coincide con `congelado` del barrido porque aquí mayoría se aprende desde cero y allá después de paridad. Lo puesto a mano: paso 0.3 y cada 200 exposiciones, un solo juego, sin barrer.
