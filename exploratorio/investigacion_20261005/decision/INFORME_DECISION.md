# INFORME DECISIÓN — pan congelado que imagina + bloque JUACO que corrige = decidir cuando el mundo cambia de regla (5-oct-2026, exploración, 10 semillas + 5 regímenes de 6)

**FUNCIONA, en un régimen concreto y con una condición que lo achica:** en un mundo de casillas donde la comida se muda (meta visible) y además las ACCIONES cambian de efecto (el modelo congelado queda medio equivocado), el conjunto "predictor congelado + planificador + bloque de células con reglas locales" rinde el 0.89 del óptimo con modelo verdadero (comida/paso 0.174 vs 0.201), **gana 10/10 semillas** al planificador con pan congelado solo (0.066: tras un cambio de regla cae a 0.001 y no recupera), a la regla a mano (0.068), al Q tabular (0.032), al bloque solo (0.027) y 9/10 al reentrenar el pan en línea con gradiente (0.114, a **1 750× más operaciones por decisión**, y rompiendo lo que no cambió: 0.84); recupera la 3ª comida tras un cambio de regla en 18 pasos [9–89] (27/30 eventos; el óptimo 12), contra 127 del gradiente y 171 del Q. El pago barajado lo baja (0.117, 9/10) y nacer con corrección al azar no lo baja nada (0.174): **lo que trabaja es el pago por acierto y la corrección local, no la memoria del nacimiento**. La condición: cuando el cambio de regla es REGIONAL (sólo la mitad izquierda), la propuesta cae a 0.68 del óptimo y empata con sus propios controles barajados (2/6): las células generalizan de más (el radio de la compuerta está puesto a mano) y pisan la mitad sana (lo intacto baja a 0.83). Y la "regla a mano" y el Q tabular, los controles que podían ganar, no ganan en ningún régimen probado; el Q se acerca (0.36 del óptimo) sólo con mundo largo y pocos cambios.

Misión: llegar a la AGI por este camino (organismo mínimo, reglas locales, con controles). Carpeta `PROYECTOS\JUACO\investigacion_20261005\decision\` (fuera de git): `decision.py` (mundo, pan con retropropagación a mano, planificador, bloque, 13 brazos, medidas), `analiza.py` (pareadas por semilla), `PREDICCIONES.md` (escritas antes; revisadas una vez tras el humo, declarado), `datos\principal.*` (10 semillas), `datos\reg_*.*` (regímenes), `datos\controles_nacimiento*.*`, `datos\eleccion_*.*` (cómo se eligieron los controles), `datos\humo*.*`. CPU total ≈ 9 min, un proceso, sin Pool.

## 1. Qué hace cada pieza (6 líneas, sin matemáticas)
1. **El mundo**: un tablero de 8×8 con una comida visible; al comerla, el agente aparece en otra casilla al azar. Cada 300 pasos la comida se muda; tres veces por vida, dos teclas intercambian su efecto (lo que era "arriba" ahora mueve a la izquierda), y nadie avisa.
2. **El pan (predictor congelado)**: una red que aprendió una vez "si estoy aquí y aprieto esta tecla, aparezco allá" (acierta el 100 % del mundo original) y nunca se vuelve a tocar. Después del cambio de tecla acierta la mitad.
3. **El planificador**: con lo que el pan imagina, calcula el camino más corto a la comida y da el primer paso; vuelve a calcular cuando la comida se muda o cuando su mapa cambia. Decide una búsqueda, no una red.
4. **La carne (bloque JUACO)**: células que viven sobre el mapa. Una nace donde el pan se equivocó ("aquí, esta tecla, caí allá"); pisa la imaginación del pan sólo donde se parece; cobra cuando su corrección acertó donde el pan fallaba; paga por existir; si pisa donde el pan ya volvió a acertar, suelta la corrección y muere; si fallan los dos, corrige lo que dice. Sin gradiente.
5. **El sueño (brazo 8)**: cada 250 pasos el pan absorbe con gradiente lo que las células corrigieron y las que ya no hacen falta se liberan (quedan 2). Rinde igual (0.175), pero el pan deja de saber lo que no cambió (0.87 [0.00–1.00]) y cuesta 33×.
6. **Los rivales**: oráculo (planifica con el mapa verdadero: la cota), regla a mano (hacia la comida con el mapa original + reflejo "si choqué, lo menos probado"), Q tabular sobre la posición relativa, reentrenar el pan en línea con búfer (el "techo" de gradiente), bloque solo sin planificador, y controles con el pago barajado y con nacimiento al azar.

## 2. Tabla principal (8×8, T=3000, sitio cada 300, 3 cambios de regla globales; mediana [mín–máx] de 10 semillas; eventos recuperados entre paréntesis)
| brazo | comida/paso | fracción del óptimo | tasa tras REGLA | 3ª comida tras SITIO | 3ª comida tras REGLA | ops/decisión | memoria | modelo vs mundo actual | intacto (lo que nunca cambió) |
|---|---|---|---|---|---|---|---|---|---|
| 0 oráculo (cota) | 0.201 [0.174–0.212] | 1.00 | 0.196 | 13 (60/60) | 12 (30/30) | 1 465 | 0 | 1.00 | 1.00 |
| 1 regla a mano | 0.068 [0.061–0.125] | 0.35 | 0.011 | 12 (32/60) | 28 (8/30) | **4** | 0 | — | — |
| 2 plan + pan congelado | 0.066 [0.056–0.120] | 0.32 | **0.001** | 11 (28/60) | 13 (4/30) | 2 901 | 0 | 0.50 | 1.00 |
| 3 Q tabular (relativo) | 0.032 [0.022–0.048] | 0.16 | 0.021 | 85 (49/60) | 171 (24/30) | 12 | 900 | — | — |
| 4 plan + pan reentrenado (techo gradiente) | 0.114 [0.091–0.135] | 0.58 | 0.022 | 20 (58/60) | 127 (18/30) | **5 949 185** | 8 576 | 0.62 | 0.84 |
| 5 bloque solo | 0.027 [0.015–0.034] | 0.14 | 0.009 | 100 (42/60) | 146 (11/30) | 56 | 40 | — | — |
| **6 pan + plan + bloque (pred)** | **0.174 [0.101–0.203]** | **0.89** | **0.162** | 13 (56/60) | **18 (27/30)** | 3 399 | 10 | 0.89 | 1.00 |
| 6c pan + plan + bloque (costo) | 0.072 [0.066–0.123] | 0.37 | 0.018 | 19 (48/60) | 60 (17/30) | 18 216 | 27 | 0.33 | 1.00 |
| 7 (6) pago barajado | 0.117 [0.106–0.163] | 0.63 | 0.077 | 15 (51/60) | 29 (23/30) | 28 076 | 32 | 0.55 | 1.00 |
| 7b (6) nace con corrección al azar | 0.174 [0.123–0.200] | 0.88 | 0.172 | 13 (56/60) | 24 (28/30) | ≈ 3 400 | 10 | 0.88 | — |
| 7c (6) barajado + nace al azar | 0.104 [0.074–0.143] | 0.52 | 0.044 | 19 (50/60) | 51 (21/30) | — | 26 | 0.42 | — |
| 8 (6) + sueño | 0.175 [0.156–0.191] | 0.88 | 0.168 | 14 (59/60) | 23 (30/30) | 112 731 | 2 | 0.51 | 0.87 [0.00–1.00] |

Pareadas por semilla (comida/paso): (6) > regla a mano 10/10 (+0.10), > plan congelado 10/10 (+0.10), > Q 10/10 (+0.14), > bloque solo 10/10 (+0.15), > techo gradiente 9/10 (+0.06), > barajado 9/10 (+0.05), > costo 10/10, = sueño 5/10, < oráculo 9/10 (−0.02). Recuperación tras regla (3ª comida): (6) más rápido que Q 10/10, que gradiente 10/10, que regla a mano 7/10. Lo peor de (6): semilla 9 (0.101): tras una rotación de 3 teclas tardó 305 pasos en la primera comida (la ventana era 300; sí recupera, lento). Paso 0 de cordura: el pan acierta 1.000 en 10/10 antes de cualquier cambio.

## 3. Regímenes (6 semillas cada uno; comida/paso de (6) como fracción del óptimo; con quién empata o pierde)
| régimen | (6) | regla mano | Q | techo grad. | barajado | ¿gana (6)? |
|---|---|---|---|---|---|---|
| principal 8×8 | 0.89 | 0.35 | 0.16 | 0.58 | 0.63 | sí (9–10/10 contra todos) |
| sitio cada 100 (cambios frecuentes) | 0.91 | 0.34 | 0.15 | 0.58 | 0.71 | sí (6/6 contra todos, 5/6 barajado) |
| mundo largo T=12 000, regla cada 3 000 | 0.96 | 0.31 | 0.36 | 0.82 | 0.56 | sí (6/6; techo 5/6): el Q mejora con tiempo pero sigue a 0.36 |
| memoria C=4 células | 0.71 | 0.35 | 0.18 | 0.58 | 0.47 | sí (5–6/6) pero cae al 0.71 |
| mundo 12×12 | 0.91 | 0.36 | 0.05 | 0.43 | 0.70 | sí (6/6): el Q y el bloque solo se hunden |
| **regla REGIONAL (mitad izquierda)** | **0.68** | 0.52 | 0.13 | **0.69** | **0.67** | **NO**: empata con el techo (2/6) y con barajado (2/6); intacto 0.83 |
| comida ESCONDIDA (humo previo) | 0.07 en todos | — | — | — | — | ningún brazo decide: todo es buscar a ciegas; se cambió el mundo (declarado) |

Dónde gana cada uno: **oráculo** siempre (es la cota). **(6)** cuando el cambio de regla es GLOBAL (una tecla cambia en todo el mapa): ahí la célula, que lee coordenadas, generaliza en una sola corrección lo que al pan one-hot y al Q les cuesta 64 visitas. **Techo de gradiente** sólo se acerca con mucho tiempo (0.82 en T=12 000) y empata en regional; nunca es barato ni limpio. **Regla a mano** y **plan congelado**: antes del primer cambio de regla son el óptimo (0.64 en las semillas donde la rotación los dejó casi intactos); después, nada. **Q tabular**: en nada de lo probado; necesita más vidas de las que hay. **Sueño**: iguala a (6) con 2 células, a 33× y rompiendo lo intacto en algunas semillas (0.00 en una). **Costo (crítico que sólo bloquea aristas)**: 0.37: saber que "ese paso no vale" sin saber adónde lleva no alcanza para replanear.

## 4. Predicciones contra lo medido
| predicción (PREDICCIONES.md, bloque revisado) | medido | |
|---|---|---|
| R1 tras sitio todos recuperan en ≤ 40 pasos en ≥ 90 % | oráculo/4/6/8 sí (93–100 %); plan congelado y regla a mano sólo 47–53 % (tras la primera regla ya no recuperan nada) | medio |
| R2 plan congelado cae a ≤ 0.05 y no recupera en ≥ 20/30; regla a mano ≤ 0.08 | 0.001, recupera 4/30; regla a mano 0.011 | sí |
| R3 (6) recupera en mediana ≤ 60 y ≥ 24/30; Q 60–200 | 18, 27/30; Q 171 | sí |
| R4 (6) > Q 8/10 y ≥ regla a mano 8/10 | 10/10 y 10/10 | sí |
| R5 techo recupera igual o mejor que (6), ≥ 100× ops, rompe original ≤ 0.6 | peor que (6) (127 vs 18 pasos, 10/10); 1 750×; pan vs original 0.41 | mejor de lo predicho para (6) |
| R6 barajado < (6) en ≥ 8/10 | 9/10 | sí |
| R7 costo < pred tras regla | 0.018 vs 0.162, 10/10 | sí |
| R8 sueño ≤ 5 células, pan vs actual ≥ 0.9, vs original < 0.8 | 2 células; vs actual 0.51 (no); vs original 0.78 (sí) | medio |
| R9 bloque solo < Q en todo | 0.027 vs 0.032 (sí, por poco) | sí |
| R10 (6) gana más claro con regla REGIONAL y sitio cada 100; Q lo alcanza en mundo largo | **al revés en regional**: ahí pierde; sitio cada 100 sí; Q no alcanza (0.36) | mitad no |
| (del humo) nacer con corrección observada es parte del mecanismo | no: nacer al azar da 0.174 = 0.174 | no esperado |

## 5. Frases que el director SÍ puede decir, y las que no
SÍ: (1) "Un predictor congelado que imagina consecuencias, un planificador que busca el camino con lo imaginado y un bloque de células JUACO con reglas locales que corrige al predictor donde el mundo cambió, se recupera de un cambio de regla en ~18 pasos y rinde el 89 % del óptimo, cuando el predictor solo cae a cero y reentrenarlo cuesta 1 750 veces más y recupera 7 veces más lento (10 semillas, 10/10)". (2) "La célula aprende dónde lo imaginado ya no vale y lo corrige; con el pago barajado se cae, y da igual con qué corrección nazca: lo que trabaja es cobrar por acertar". (3) "El sistema decide por búsqueda sobre un modelo del mundo: 'planea' y 'modelo del mundo' aguantan en este juguete (es iteración de valor sobre 64 casillas; el modelo es una tabla de 256 transiciones)". (4) "Las células no rompen lo que el predictor sabía (1.00 en lo intacto) cuando el cambio es global".
NO: "decide" en el sentido de elegir metas (la meta la da el mundo: la comida visible; no hay hambre ni costo intrínseco que la elija), "aprende el mundo" (el pan lo aprendió con gradiente antes; las células sólo parchan), "gana a Q en general" (Q estaba famélico: 3 000 pasos, 900 estados; con T=12 000 sube a 0.36 y seguiría subiendo), "sirve con cambios locales" (regional: empata con el barajado; el radio de la compuerta, 0.5, está puesto a mano y generaliza de más), "funciona con comida escondida" (ahí nadie decide), "es JEPA" (el pan predice la casilla siguiente, no una ficha latente; no hay codificador), "más barato que la regla a mano" (4 ops vs 3 400).

## 6. Qué ya existe con otro nombre, y en qué se diferencia lo construido
- **Dyna / planificación con modelo tabular** (Sutton 1990): lo más parecido: modelo aprendido + iteración de valor; aquí el modelo es una red congelada y el parche lo ponen células con vida (nacen, cobran, mueren, sueltan), no una tabla que se sobrescribe.
- **MuZero**: aprende modelo, valor y política con gradiente para buscar; aquí nada se aprende con gradiente en uso.
- **Dreamer v3 / TD-MPC2**: imaginan en latente para entrenar o planificar una política con gradiente; aquí el latente es la casilla y no hay política entrenada.
- **DINO-WM / V-JEPA 2-AC**: codificador congelado + predictor + búsqueda con meta dada en imagen: la misma forma "congelado + buscador + meta externa"; se diferencia en que el predictor de ellos nunca se corrige en uso; aquí las células lo corrigen y sueltan.
- **Model-based RL con detección de cambio / "surprise" (p.ej. MBCD)**: reaprenden el modelo cuando sorprende; aquí la sorpresa hace nacer una célula local y la selección económica decide cuál queda.
- **Crítico de LeCun (costo intrínseco + crítico aprendido)**: la variante 6c (célula corrige el costo) es eso en chico; perdió contra corregir la predicción (0.37 vs 0.89).

## 7. Siguiente paso más chico
Una tarde: **compuerta con radio propio por célula** (empieza ancha y se estrecha cada vez que pisa donde el pan acertaba), probada SOLO en el régimen regional, con el barajado y el "nace al azar" como controles; criterio: (6) > barajado en ≥ 5/6 semillas y lo intacto ≥ 0.95; si no, el bloque no sirve para cambios locales y se dice. Después, si eso sale: meta NO dada (hambre interna que elige entre dos comidas) para poder decir "decide".

## 8. Lo que puse a mano, cómo reproducir, lo no verificado
- A mano: comida visible (tras ver el humo con comida escondida: declarado); rasgos de la célula = (x/8, y/8, tecla) con radio 0.5 y compuerta 0.5 (sin barrido; es lo que hace que generalice el cambio global y que falle el regional); existir 0.002, pago 1, castigo 0.5, mezcla 0.3 (del informe 3); planificador = iteración de valor 40 barridos; Q (α 0.5, ε 0.2, Q0 0) y techo (búfer 128, lote 32, lr 3e-3) elegidos entre 3 variantes cada uno con 2 semillas (`datos\eleccion_*.txt`; el Q con otras perillas daba 0.018–0.022; el techo 0.085–0.114); sueño cada 250, 30 pasos, lr 1e-3 con pseudo-ensayo; "recuperar" = 3ª comida tras el evento dentro de la ventana hasta el siguiente evento; ops = multiplicaciones-sumas aproximadas (pan 16 896 por predicción; planificador 512 por barrido).
- Reproducir (≈ 65 s): `cd PROYECTOS\JUACO\investigacion_20261005\decision; python decision.py --semillas 10 --brazos "0 oraculo,1 regla_mano,2 plan_pan,3c q_rapido,4c plan_pan_grad_bufer_lr3,5 bloque_solo,6 plan_pan_cel,6c plan_pan_cel_costo,7 plan_pan_cel_baraj,8 sueno" --out datos/principal.json; python analiza.py datos/principal.json`. Regímenes: `--regional`, `--cada_sitio 100`, `--T 12000 --cada_sitio 600 --reglas 3000,6000,9000`, `--C 4`, `--N 12 --cada_sitio 400 --T 3600 --reglas 1200,2400`. Humo: `python decision.py --humo`.
- No verificado: sin preregistro formal (predicciones escritas antes, revisadas una vez tras el humo, con el bloque original visible); 10 semillas, sin réplica; un juego de perillas de la célula; el pan es one-hot (sin generalización espacial), lo que favorece a las células frente al techo de gradiente: con un pan por coordenadas (`--pan coord`, 2 semillas, `datos\eleccion_techo_coord.txt`) el techo tampoco recupera (0.04 tras regla) pero no se corrió la serie completa; el Q tabular no se corrió hasta converger; el "techo" es reentrenar en línea, no un ajuste fino serio; semilla 9 (305 pasos para recuperar) no diagnosticada a fondo; las 3 rotaciones son acumulativas (en algunas semillas una rotación deshace otra: por eso regla a mano llega a 0.125 en 2 semillas); el régimen regional es el único cambio "parcial" probado; el sueño rompe lo intacto en 1 semilla a 0.00 sin diagnóstico. Incidente de procedimiento: para detener mi propia serie usé una vez `taskkill /IM python.exe` con un filtro; verifiqué después que NO mató nada (la serie de 6 h `corre_muro_perillas.py` y los procesos de JUACO-OPENEVOLVE siguieron vivos, con hora de creación anterior); queda anotado como error mío de procedimiento.
