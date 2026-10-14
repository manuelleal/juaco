# PREREGISTRO — MURO MÍNIMO, PIEZA POR PIEZA (13-oct-2026; escrito ANTES de correr las semillas selladas)

Misión: llegar a la AGI por este camino. Este bloque es consolidación: saber **cuál** de las piezas que MINIMO omitió de HUMO cierra la
brecha, de una en una, para decidir si el "órgano del muro" es **dos modos + una pieza concreta** o algo más enredado.

Antecedente (`experimentos/muro_minimo_20261008/`, HAY ALGO MODESTO ×2): MINIMO (dos modos a mano sobre O1 sin limpieza) con mayoría
en 10/20 y 11/20; HUMO 20/20 ×2; KO_PIZARRA (HUMO sin pizarra) 18 y 19/20; linajes MINIMO 87 y 94 contra HUMO 155 y 151 y KO_PIZARRA
122 y 123. Lo que NO se hace aquí: ajustar MINIMO sobre las semillas usadas (283001–283040), ni declarar falsa la lectura de dos
modos sin separar las piezas.

## 1. Hipótesis
Una sola de las cuatro piezas de §2 del preregistro anterior, añadida a MINIMO en su forma de HUMO y sin nada más, basta para cruzar
el muro como HUMO (mayoría en ≥ 15/20). Hipótesis rival: ninguna sola basta (la brecha es una combinación).

## 2. Brazos y piezas (una pieza por brazo; todo trozo nuevo sale de `HUMO.py` por ancla, salvo la llave)

| brazo | pieza (§2 del bloque anterior) | qué añade a MINIMO, en llano | código | sha12 | llave |
|---|---|---|---|---|---|
| MINIMO | — | el carro del bloque anterior, mismo texto (sha16 b9cfbb3bb7cb3de6) | 100 líneas | b9cfbb3bb7cb | — |
| M_PIZARRA | **P1 pizarra** | escucha lo que otros linajes publican sobre una letra (por su código) y publica por turno dos letras que conoce; un fundador sin memoria ya "sabe" lo que otros saben | +46/−3 | 1f320504565f | P_PIZARRA |
| M_RADIO | **P2 radio de banco** | cerca de criar no persigue nada a más de 45 casillas (RADIO_BANCO) y castiga fuerte la distancia (D0_BANCO 0.6 en vez de 3.0) | +5/−1 | f886a5ff8c88 | P_RADIO |
| M_RECICLA | **P3 utilidad de limpiar** | lejos de criar, limpiar lo malo conocido entra en la competencia del blanco con puntaje RECIC_UTIL 0.6/(d+3) (con la penalización por otro cuerpo más cerca): lo malo cercano le gana a lo bueno lejano y a probar lo desconocido. En MINIMO limpiar era el último recurso | +6/−0 | fbd7cfc330f2 | P_RECICLA |
| M_URGENCIA | **P4 urgencia** | la urgencia de una reserva sobre el umbral pesa 1.3 en vez de 1.0 en la ganancia | +2/−1 | 54a34b7207bc | P_URGENCIA |
| HUMO | — (control alto) | sha16 69fcfcb2473fdbf6 | 159 líneas | 69fcfcb2473f | — |

P2 lleva dos números (radio y suavizado) porque §2 los declaró como UNA pieza; no se separan aquí (ver §6, dudas).
Memoria nueva: cero en P2, P3, P4; P1 añade lo que HUMO tiene (tabla código → valor medio y turno de difusión), sin costo de escritura
en la pista.

**No son brazos (sólo identidad):** AUX_TRES = MINIMO + P2 + P3 + P4 (debe ser KO_PIZARRA bit a bit) y AUX_TODAS = MINIMO + P1–P4
(debe ser HUMO bit a bit). Si lo son, la lista de §2 del bloque anterior es **completa**: entre MINIMO y HUMO no hay una quinta
diferencia escondida, y la pregunta "¿cuál pieza?" está bien planteada.

## 3. Instrumento, anclas e identidad
- `construye.py` (+ `construye_examen.py`): copia sin reemplazos, con sha fijado, `corre_carro.py` y `evaluador.py` del examen grande
  (`openevolve_serie/`), MINIMO del bloque anterior, HUMO, KO_PIZARRA y `coteja_preregistro.py` (METODO); escribe cada variante desde
  MINIMO con parches de ancla única y comprueba que cada trozo nuevo está en HUMO; construye `corre_examen.py` por anclas desde el del
  bloque anterior (sha d202bd621d2eb4ba): cambian docstring, constantes, `letra`, argumentos y cabecera; la llamada a `corre_carro.py`
  (`una`) y la línea `P.run(...)` quedan byte a byte (regla 14: 9 copias, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador no
  limpio). `--check` sale con 1 si algo difiere.
- `identidad.py` (T 5 000, semillas 884901–884903): (a) MINIMO de aquí == MINIMO del bloque anterior con SU `corre_carro.py`;
  (b) cada brazo con su llave en 0 == MINIMO; (c) AUX_TODAS con las cuatro llaves en 0 == MINIMO; (d) AUX_TODAS == HUMO y
  AUX_TRES == KO_PIZARRA; todos los campos del JSON menos `seg`, incluido `rng_mundo_estado`. (e, descriptivo) cada brazo encendido
  difiere de MINIMO en 5 000 pasos.
- `corre_examen.py` se niega a correr si `construye --check`, un sha12, el filtro de reglas o el **cotejo PREREGISTRO.md ↔
  PREREGISTRADO** (sección «Parámetros sellados») fallan. Fuera de `--humo` sólo acepta las dos tandas de §4 con los 6 brazos y T 100 000.
- T 100 000, fundador no limpio, 9 copias del carro por corrida (como el bloque anterior).

## 4. Semillas
- **Serie 885001–885020. Réplica 885021–885040 (decisión del coordinador antes del commit: 884001–884020 estaban reservadas por muro_perillas; 885001–885040 están limpias).** Grep del 13-oct (.py/.md/.txt, nombres de archivo): ningún archivo de corrida con
  esas semillas. **Aviso:** 884001–884020 aparecen en `organelos/muro_perillas/PREREGISTRO_muro_perillas.md` como pruebas de una
  "segunda serie fl 0 (si se decide)" que nunca se corrió. El coordinador pidió 884001; si prefiere no pisar esa reserva, el rango
  limpio es 885001–885040 (sin apariciones), y se cambia ANTES del commit del preregistro.
- Humo: 884901, T 20 000, una corrida por brazo (6), un proceso. Identidad: 884901–884903, T 5 000.

## 5. LA LETRA
"Con mayoría" = `cruzan_real` ≥ 5/9 en la semilla (cruza_real del juez = R0 real ≥ 0.90 y 0 fundadores tras t = 10 000).
**Por tanda (20 semillas):**
- Validez: V1 120/120 corridas; V2 shas, filtro y cotejo (el runner se niega si no); **V3: HUMO con mayoría en ≥ 15/20.**
- **Control bajo que puede fallar, C1: MINIMO con mayoría en ≤ 14/20.** Si MINIMO cruza, no hay brecha que cerrar en estas semillas.
- Si falla V o C1 → NO SE LEE.
- Por brazo de pieza: **CIERRA** = mayoría en ≥ 15/20 · **MUEVE** = no cierra y suma de linajes que cruzan ≥ la de MINIMO + 20 (mismas
  semillas) · **NADA** = lo demás.
- Tanda: FUNCIONA si alguna pieza CIERRA; HAY ALGO MODESTO si ninguna cierra y alguna MUEVE; NO si ninguna.

**Bloque (serie + réplica; `corre_examen.py --combina`):** cada pieza vale el MENOR de sus dos estados (CIERRA > MUEVE > NADA).
**FUNCIONA** = alguna pieza CIERRA ×2 · **HAY ALGO MODESTO** = ninguna CIERRA ×2 y alguna al menos MUEVE ×2 · **NO** = ninguna MUEVE ×2
· **NO SE LEE** si alguna tanda lo es. Si cierran dos, se reportan las dos (redundancia), no se elige.

**Placebo de cada puerta (regla 15)**, con los 40 + 40 datos del bloque anterior (n = 20 por tanda):

| puerta | nulo | P(pasa \| nulo) | P(pasa \| alternativa) |
|---|---|---|---|
| CIERRA ≥ 15/20 | brazo = MINIMO (21/40 semillas con mayoría, p 0.525) | 0.035 | 0.997 si p = 0.925 (KO_PIZARRA); 0.62 si p = 0.75 |
| MUEVE ≥ +20 linajes | mismo organismo (bootstrap de MINIMO: sd por semilla 1.52, sd de la diferencia 9.6) | 0.020 | 0.92 si es como KO_PIZARRA (+1.6/semilla); 0.52 si +1/semilla |
| C1 MINIMO ≤ 14/20 | MINIMO como antes | cumple 0.965 | — |
| V3 HUMO ≥ 15/20 | HUMO como antes (40/40; p 0.95) | cumple 0.9997 | — |

Comparaciones múltiples: con 4 brazos nulos, P(alguno CIERRA en una tanda) ≈ 0.13; **la misma pieza ×2 ≈ 0.005**; MUEVE ×2 ≈ 0.002.
Correlación por semilla entre brazos (MINIMO contra KO_PIZARRA, 40 semillas): −0.13, así que las tandas se tratan como independientes.
Margen: MUEVE pide ≈ +1 linaje por semilla; una pieza que dé sólo la mitad de eso (+0.5/semilla) saldrá NADA con probabilidad alta. Es
el precio de un nulo de 0.02; se dice antes de correr.

**Se reporta sin decidir:** pareado de cada brazo contra MINIMO y contra HUMO; medianas de R0 real, vida, muertes, mordidas malas,
limpiezas físicas, fracción de pasos sin nada bueno, fundadores tras t = 10 000; causas de muerte y mordidas por letra.

## 6. Predicciones (escritas antes del humo; mayoría /20 y linajes por tanda)

| # | predicción | rango | p |
|---|---|---|---|
| Q1 | MINIMO: mayoría 10/20, linajes ≈ 90 | 7–13; 78–102 | 0.80 |
| Q2 | HUMO: mayoría ≥ 18/20, linajes ≈ 153 | 18–20; 138–166 | 0.85 |
| Q3 | **M_RECICLA CIERRA ×2**: mayoría ≈ 15/20, linajes ≈ 115 | 12–18; 100–132 | 0.40 |
| Q4 | M_RECICLA al menos MUEVE ×2 | — | 0.65 |
| Q5 | M_RADIO: mayoría ≈ 12/20, linajes ≈ 102 | 8–16; 86–118 | 0.60 (CIERRA ×2: 0.12) |
| Q6 | M_PIZARRA: mayoría ≈ 11/20, linajes ≈ 98 | 8–14; 84–112 | 0.60 (CIERRA ×2: 0.07) |
| Q7 | M_URGENCIA: mayoría ≈ 10/20, linajes ≈ 90 (no se distingue de MINIMO) | 7–13; 78–104 | 0.75 (CIERRA ×2: 0.02) |
| Q8 | mordidas malas (mediana) de M_RECICLA entre 8 000 y 9 800 (MINIMO ~6 900, HUMO ~9 000) | — | 0.60 |
| Q9 | identidad: AUX_TODAS == HUMO y AUX_TRES == KO_PIZARRA bit a bit | — | 0.85 |
| V | bloque FUNCIONA / MODESTO / NO / NO SE LEE | — | 0.42 / 0.25 / 0.28 / 0.05 |

**Pieza que espero que cierre: P3 (utilidad de limpiar).** Razón, con los datos del bloque anterior: MINIMO muerde menos lo malo
(mediana ~6 900 contra ~9 000 de HUMO y KO_PIZARRA; limpiezas físicas 6 300 contra 8 400) **y también menos lo bueno** (A y C ≈ 4 700
contra ≈ 5 750: un 18 % menos de comida), y muere más de hambre y sed (≈ 140 contra ≈ 100–110 por tanda). Eso es lo que hace un carro que
sólo limpia cuando no queda nada bueno en todo el anillo (el 82 % del tiempo queda algo): viaja a lo bueno lejano dejando lo malo cerca,
el mundo repone menos y la comida que encuentra al llegar ya se la comió otro. P3 es justo la regla que cambia eso, y su firma
predicha (más mordidas malas, más A+C, menos muertes de hambre) se puede leer en el humo antes de las selladas.

**El mejor argumento de que ninguna sola la cierra:** HUMO salió de una búsqueda que ajustó las cuatro piezas **juntas** (OpenEvolve);
RECIC_UTIL 0.6 está calibrado contra ganancias con urgencia 1.3 y contra el radio de banco: P3 sin P4 hace limpiar un poco más
atractivo que en HUMO, y P3 sin P2 deja a los cuerpos que ya crían cazando comida lejana mientras los que no crían limpian. Si la brecha
es de dos fallas distintas (hambre lejos de criar → P3; racha rota o comida acaparada cerca de criar → P2), cada pieza sola recupera la
mitad (+0.6 linajes por semilla, ~+12 por tanda), queda bajo +20 y bajo 15/20, y el bloque sale **NO** aunque la lectura de dos modos
más dos piezas sea correcta. Por eso Q3 está en 0.40 y no más.

## 7. Qué diría cada veredicto (y qué no)
- **FUNCIONA (pieza X CIERRA ×2):** "en la pista vieja con fundador no limpio, la decisión de dos modos escrita a mano más la pieza X de
  HUMO, y nada más, cruza el muro en ≥ 15/20 semillas ×2". El órgano del muro de HUMO es dos modos + X. No diría que X sea la única
  forma, ni que sea aprendido o evolucionado (es diseño), ni que MINIMO + X sea mejor que HUMO o que O1.
- **HAY ALGO MODESTO (alguna MUEVE ×2, ninguna CIERRA ×2):** "X empuja (≥ +20 linajes ×2) pero no basta sola: hace falta más de una
  pieza". Siguiente bloque: pares, o quitar una a una desde AUX_TRES (= KO_PIZARRA, que cruza 37/40).
- **NO (ninguna MUEVE ×2):** "ninguna pieza sola mueve la brecha de forma detectable con n = 20": el órgano es una combinación (enredado).
  **No** diría que las piezas no importan (la disección de HUMO las hizo necesarias en bloque) ni que la lectura de dos modos sea falsa.
- **NO SE LEE:** HUMO bajo 15/20, MINIMO en ≥ 15/20 (sin brecha) o corridas incompletas: no se declara nada.

## 8. Las cuatro trampas
- Canal simétrico: en M_PIZARRA los 9 linajes son copias que escriben y leen igual (lo mismo que HUMO); en los demás brazos nadie
  escribe (`escrituras` = 0 en el JSON, se comprueba en el humo). No hay un brazo "mudo contra hablante" que leer.
- Acierto sin balancear: la medida es mayoría de linajes por semilla con control bajo (MINIMO) y alto (HUMO), y placebo de cada puerta
  (§5). No hay tasa de acierto.
- Mundo que se come la comida: **es el fenómeno**; P3 cambia a propósito cuánto se limpia. Se reportan mordidas por letra, limpiezas,
  fracción de pasos sin nada bueno y composición del mundo; si M_RECICLA cruza dejando el mundo más pelado, se dice.
- Sitios fijos: los objetos reaparecen al azar; ningún carro guarda posiciones.

## 9. Costo y parada
0 USD. 120 corridas por tanda; MINIMO ~400–650 s y HUMO ~250–390 s por corrida de 100 k (bloque anterior, pool 3) → ≈ 2.5–3.5 h por
tanda con pool 3. Serie y réplica; no hay más tandas. ERR nuevo: ninguno al escribir esto; siguiente libre ERR-203.

## Parámetros sellados
| nombre | valor | de dónde |
|---|---|---|
| BRAZOS | ["MINIMO", "M_PIZARRA", "M_RADIO", "M_RECICLA", "M_URGENCIA", "HUMO"] | §2 |
| PIEZAS | ["M_PIZARRA", "M_RADIO", "M_RECICLA", "M_URGENCIA"] | §2 |
| SHAS | {"MINIMO": "b9cfbb3bb7cb", "M_PIZARRA": "1f320504565f", "M_RADIO": "f886a5ff8c88", "M_RECICLA": "fbd7cfc330f2", "M_URGENCIA": "54a34b7207bc", "HUMO": "69fcfcb2473f"} | §2 |
| SERIE | range(885001, 885021) | §4 |
| REPLICA | range(885021, 885041) | §4 |
| N_LETRA | 20 | §5 |
| T_LETRA | 100000 | §3 |
| MAY | 5 | §5 |
| CIERRA_MIN | 15 | §5 |
| MUEVE_LIN | 20 | §5 |
| C1_MINIMO_MAX | 14 | §5 |
| V_HUMO_MIN | 15 | §5 |
| HUMO_SEMILLA | 884901 | §4 |
| HUMO_T | 20000 | §4 |

Firmado: Claude (creador), 13-oct-2026, escrito mientras corría la identidad dinámica (sin mirar su salida) y antes del humo;
ninguna semilla sellada corrida.

## 11. Identidad y humo (añadido tras correrlos, 13-oct ~19:45; §1–§10 no se tocaron)
- `identidad.py` (T 5 000, 884901–884903, 37 corridas de un proceso): **ARNÉS PASA, puertas 24/24.** (a) MINIMO de aquí == MINIMO del
  bloque anterior con su `corre_carro.py` 3/3; (b) cada brazo con la llave en 0 == MINIMO 12/12; (c) AUX_TODAS apagada == MINIMO 3/3;
  (d) **AUX_TODAS encendida == HUMO 3/3 y AUX_TRES encendida == KO_PIZARRA 3/3** (33/33 campos, `rng_mundo_estado` incluido; HUMO con
  ~44 960 escrituras en 5 000 pasos). La lista de §2 del bloque anterior es completa: MINIMO + P1–P4 ES HUMO. Q9 se cumple.
  (e) cada brazo encendido difiere de MINIMO en 5 000 pasos (4/4): las cuatro piezas actúan.
- Humo `corre_examen.py --humo` (884901, T 20 000, 6 corridas, un proceso, 596 s; escribe `humo/s884901-884901_T20000/*.json` y
  `resumen.json`): el runner pasa construye, shas, filtro y cotejo (14/14). **A T 20 000 nadie cruza** (HUMO 0/9 también): `cruza_real`
  no se puede leer tan corto; el humo prueba la tubería, no el cruce. Descriptivo, una semilla, nada se declara:

| brazo | persisten | vida med | muertes (hambre+sed) | A+C | mord. malas | limpiezas | fund. | escrituras |
|---|---|---|---|---|---|---|---|---|
| MINIMO | 4/9 | 1 401 | 72 (60) | 1 952 | 1 491 | 1 361 | 22 | 0 |
| M_PIZARRA | 5/9 | 1 648 | 71 (60) | 1 819 | 1 347 | 1 198 | 16 | 179 956 |
| M_RADIO | 4/9 | 1 401 | 80 (70) | 1 785 | 1 268 | 1 150 | 28 | 0 |
| M_RECICLA | 2/9 | 3 431 | 42 (30) | 2 373 | 1 802 | 1 663 | 5 | 0 |
| M_URGENCIA | 7/9 | 1 309 | 76 (66) | 1 936 | 1 446 | 1 314 | 26 | 0 |
| HUMO | 1/9 | 4 134 | 32 (27) | 2 521 | 2 021 | 1 880 | 1 | 179 956 |

  En esta semilla y este largo, sólo M_RECICLA se mueve hacia HUMO en la firma que §6 predijo para P3 (más A+C, más limpieza, la mitad
  de muertes de hambre y sed, vida 2.4× la de MINIMO). Las predicciones de §6 se dejan como están.
