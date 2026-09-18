# BORRADOR — NO COMMITEADO. Nivel 6 en 2D: ¿rodea de verdad, mira más allá de un paso, encadena dos metas?

**Escrito por el diseñador (agente) el 18 sep 2026, madrugada. Es un BORRADOR para el coordinador:** no se ha corrido
ninguna serie, no hay declaración, y nada de esto entra al registro hasta que el coordinador lo convierta en bloque
preregistrado (regla 7 de `registro/EQUIPO.md`). Continúa `experimentos/nivel6_mapa/PREREGISTRO_mapa.md` y
`experimentos/nivel6_rodeo/PREREGISTRO_rodeo.md` (+ enmienda 1), y ataca exactamente lo que el anillo dejó abierto
(`registro/HANDOFF.md` §13, fila nivel 6): *secuencia de acciones (ir a A y luego a B), rodeo falso, `M` que se degrade*.
Los humos declarados están al final (§Declaración); **ningún criterio sale de ellos**.

## 0. Por qué 2D, y qué se descubrió al diseñarlo (esto va al registro pase lo que pase)

1. **En un anillo la dirección ya integra todo el horizonte.** `_sesgo_M` reparte lo recordado en dos montones
   (izquierda / derecha) que **parten el mundo entero**: no hay forma de distinguir horizonte 1 de horizonte 2, ni de
   exigir una secuencia, ni de construir un obstáculo (en un anillo *toda* desviación llega igual). Por eso el nivel 6
   se declaró *"elige … no planifica"* y no se puede hacer más en ese mundo.
2. **La generalización exacta a 2D del sesgo no es "sumar por filas y columnas".** La regla del anillo, escrita sin
   coordenadas, es: *cada celda recordada a distancia `h` suma `disc^h·valor` a toda acción que la ACERQUE* (la celda
   antipodal, que el anillo cuenta en las dos direcciones, es el caso de empate). Esa forma se traslada tal cual a la
   distancia toroidal Manhattan y **se reduce término a término, y en el mismo orden de suma, a la del anillo con
   `alto=1`** (por eso la identidad sale bit a bit). En 2D una celda en diagonal suma a **las dos** direcciones que la
   acercan: el sesgo es un **cono**, no un rayo.
3. **Consecuencia no prevista en el anillo: en 2D el mecanismo es un VOTO GLOBAL.** Con `disc = 0.9` y `H_M = 20`, en
   una rejilla de 17×13 toda celda recordada está a distancia ≤ 15 y pesa ≥ 0.9¹⁵ = 0.21. **No existe "lejos"**: toda
   la geometría de §2 está calculada con *todos* los sitios, no con el de interés.
4. **El veneno recordado no repele el camino: repele el ACERCAMIENTO.** Una barrera resta a toda acción que acerque a
   cualquiera de sus celdas, la vayas a pisar o no. De ahí la predicción central: **el mecanismo actual no rodea, se aleja.**
5. **`v_B` no es una constante del organismo, es una propiedad del MUNDO.** Medido en el humo: con 4 sitios de veneno
   de 5, `v_B ≈ −2.3` en 3/3 semillas; con 1 sitio de veneno de 2, `v_B = +0.10` (¡positivo!: casi nunca lo muerde, la
   puerta manda a la vía lenta y ésta generaliza desde A). Cualquier prueba 2D cuya predicción dependa del cociente
   `r = |v_B|/v_A` tiene que fijar el mundo **y** declarar su ventana de validez por semilla (§5, V-T2).

## 1. Instrumento: `experimentos/nivel6_2d/mundo_2d.py` (`683b45c743b589c3`, 320 líneas)

Generado por `construye_2d.py` **por anclas con conteo exacto** (12 parches, cada una exactamente una vez) desde
`mundo_mapa_rodeo.py` (**sha `7ab34aed9acffaa0`**, que a su vez es `mundo_mapa.py` **`207d6a1954336b18`**; los dos shas
están fijados en el constructor y se comprueban al generar). Se construye desde el *rodeo* y no desde el *mapa* porque
el ancla pedida incluye la identidad con `modo='rodeo'`: así las dos anclas viven en un solo linaje.

**El organismo no cambia**: ni `valor()`, ni la boca, ni el aprendizaje, ni las dos vías, ni la puerta. Cambian tres
cosas, todas del MUNDO: (a) la posición es un índice plano sobre una rejilla toroidal `ancho × alto`
(`x = pos%ancho`, `y = pos//ancho`) y hay 4 acciones (`0=−x, 1=+x, 2=−y, 3=+y`); (b) la retina sigue viendo **el objeto
más cercano**, ahora en distancia toroidal Manhattan, y su lado se codifica como **un bit por dirección** (one-hot);
(c) `M` es posición 2D → patrón y el sesgo es el cono de §0.2. Toda la geometría de las pruebas vive **dentro de
`prueba`**; `alto=1` es el anillo del tronco.

**Reglas deterministas que hubo que fijar (no había equivalente en el anillo):**
- *Más cercano*: `d = min(|Δx|, ancho−|Δx|) + min(|Δy|, alto−|Δy|)` (Manhattan toroidal).
- *Empate de distancia entre objetos*: gana el **primero de `objs`** (orden de inserción), exactamente como en el anillo.
- *Dirección que informa la retina*: **eje dominante** (`dx ≥ dy` → eje x, empate → x); dentro del eje, el lado corto,
  y el empate de lado va a `+x`/`+y` — que es justo lo que hace el `dl<dr` del tronco (con `dl == dr`, y también en
  contacto, v13 enciende el bit "derecha").

**ANCLA DE IDENTIDAD — resultado: `identidad_2d.py` → 51/51 corridas idénticas** (T = 20 000, semillas 1–3, un proceso,
337 s). Tres rejillas, comparando **todos los diccionarios de salida** tras ida y vuelta por JSON:

| rejilla | qué compara | configuraciones | resultado |
|---|---|---|---|
| 1 | `mundo_2d(alto=1)` ≡ `mundo_mapa` | 11 (apagadas, apagadas+inversión, MAPA, SINMAPA, CONGELADA, BARAJADO, INVERTIDO, `M` sin sitios con muchas celdas, perillas `H_M/disc_M/gamma_M/regen`, divisiones vivas, sólo `r_vis`) × 3 semillas | **33/33** |
| 2 | `mundo_2d(alto=1, modo='rodeo')` ≡ `mundo_mapa_rodeo` | 3 (rodeo, rodeo invertido, otras `g/dps/aas`) × 3 | **9/9** |
| 3 | `mundo_2d` con perillas apagadas ≡ `organismo_v13` | 3 (base, `nuevo='C'`, v11) × 3, claves de v13 + `tel=None`, `M_llenas=0` | **9/9** |

La identidad **sí** es alcanzable sin cambiar el orden de consumo del `rng`, y eso obligó a tres decisiones de diseño:
`Wl` es `(_NA, _NF)` = `(2, 9)` con `alto=1` (mismo primer `uniform`); el ruido de la política es
`rng.normal(0,.3,_NA)` (mismo consumo por paso); y el sesgo acumula **por distancia creciente** (mismo orden de suma en
punto flotante que el generador `h = 1..H_M` del anillo). **No se añade ni se quita ninguna clave de salida.**

## 2. Mundo, montaje y las cuatro pruebas

Rejilla **17 × 13 = 221 celdas**, `r_vis = 3`, sitios fijos con `regen = 50`, `T = 100 000`, `gamma_M = 0.6`,
`disc_M = 0.9`, `H_M = 20` (todo del mapa del anillo; **nada recalibrado**). Los sitios se colocan por coordenadas
relativas a un **origen azaroso por semilla** y **reflejados (punto de reflexión, 0↔1 y 2↔3) en las semillas pares**.
`M` se escribe sólo al pisar un sitio ⇒ al acabar el entrenamiento `M` tiene exactamente tantas entradas como sitios
(V1). Después, **sin aprendizaje y sin boca**, 40 teletransportes por semilla; en cada uno se mide la **dirección del
primer paso**, el vector de sesgo `B` completo de ese instante (y el de horizonte 2), si **llega** a una comida, si
**pisa** veneno (más estricto que morderlo: no se consulta la boca) y cuántas comidas distintas alcanza. `E_test = 0.3`,
traza y memoria de rechazo a cero, sitios repuestos antes de cada episodio. **En los cuatro casos todo sitio está a
distancia ≥ 4 del punto de partida** (> `r_vis`): la retina arranca vacía y sólo `M` puede decidir; se verifica con
`ciego_al_llegar = 40/40`.

| mundo | sitios (coordenadas relativas) | prueba | S | acción correcta |
|---|---|---|---|---|
| **M1 barrera** | comida (0,0); veneno (2,−2),(2,−1),(2,0),(2,1) | **T1 rodeo VERDADERO** | (6,0) | camino limpio más corto = 10 pasos por arriba ⇒ **{−x, +y}**; el flanco barato es +y (por abajo son 12) |
| **M2 sombra** | comida (0,0); veneno (2,0),(3,0); comida (−4,−4) | **T4 rodeo FALSO** | (−4,0) | las **dos** comidas están a 4 pasos limpios: +x (con veneno *detrás* de ella) y −y (limpia): son equivalentes |
| **M3 flanco** | comida (4,0); veneno (1,6) *[el del flanco]*; veneno (0,5) y (0,−5) *[dieta: `Δx = 0`, no tocan ±x]* | **T2 HORIZONTE 2** | (0,0) | **{+x}** (4 pasos limpios; el veneno no está en el camino) |
| **M4 secuencia** | comida (0,0); comida (4,0); veneno (−4,4) | **T3 SECUENCIA A→B** | (−4,0) | **{+x}**: A a 4 pasos, B 4 pasos más allá, todo limpio |

**Qué pregunta cada una.**
- **T1** — obstáculo (de veneno recordado, el único obstáculo que este organismo puede representar) entre él y la meta.
  Rodear exige un primer paso que **no acerca** a la comida.
- **T2** — el veneno del flanco está a un paso de salirse del cono (su `Δx` pasa de +1 a 0): la mejor acción **a un
  paso** no es la mejor **a dos**. Los otros dos venenos están alineados en x con S (`Δx = 0`), así que **suman lo mismo
  a +x y a −x** (de hecho, nada) y sólo sirven de dieta para que `v_B` se aprenda (§0.5).
- **T3** — encadenar: llegar a A, comérsela y seguir a B. La comida alcanzada **se consume** dentro del episodio.
- **T4** — el veneno está **detrás** de la comida, donde nunca lo pisaría; la otra comida, idéntica y a la misma
  distancia, está limpia. Si prefiere la limpia, se desvía **sin motivo**.

## 3. Mecanismos que se ponen a prueba (ninguno toca el organismo)

- **H1 — el actual, extendido a 4 direcciones** (bit a bit el del anillo con `alto=1`):
  `B_a = Σ_{c ∈ M, 1 ≤ d(pos,c) ≤ H_M, d(pos+a, c) = d−1} disc^{d(pos,c)} · valor(M[c])`, y `u += gamma_M · B`
  sólo con la retina vacía. **Coste:** una pasada por las celdas escritas de `M`; **memoria:** la que ya tiene.
- **H2 — candidato de horizonte 2 (perilla `h2` dentro de `prueba`):**
  `Q_a = B_a(pos) + disc_M · max_{a'} B_{a'}(pos + a)` — *simular un paso con `M` y evaluar desde ahí*.
  **Coste explícito:** `1 + 4 = 5` evaluaciones del sesgo por paso (×5 sobre H1), cada una O(celdas de `M`); medido,
  ×1.3 sobre el tiempo total de una corrida (el lookahead sólo corre en los 40 episodios).
  **Memoria explícita:** una posición simulada; **ninguna estructura nueva**, ni traza, ni valor nuevo. No hay "quedarse
  quieto": el máximo es sobre las 4 acciones.
- **H3 — candidato mínimo para T3 (perilla `borra_M`):** *el mapa se corrige con lo que veo*: estando en una celda que
  `M` recuerda y que está **vacía**, se borra esa entrada. Una línea, sin memoria nueva. Sin él, `M` sigue diciendo
  "aquí hay comida" después de habérsela comido.

## 4. Brazos (por mundo)

| brazo | qué es | esperado |
|---|---|---|
| **MAPA** | v13 + `M`, mecanismo H1 | la pregunta |
| **MAPA_h2** | mismo entrenamiento, decisión por H2 | la comparación de mecanismo |
| **SINMAPA** | v13 en el mismo mundo, sin `M` | **0.25 por acción por construcción**: con la retina vacía `x = 0`, `V = Wl@x = 0`, `p` igual en las 4 patas ⇒ decide sólo el ruido `N(0,.3)` |
| **CONGELADA** | `M` nunca escrita | **≡ SINMAPA bit a bit** (el sesgo es el vector cero); se verifica `M_llenas = 0` |
| **INVERTIDO** | MAPA con `Wp↔Wn`, `Wps↔Wns` en la prueba (la puerta usa \|Wp−Wn\| y no cambia) | control decisivo: con el valor del revés debe **ir hacia el veneno** |
| **BARAJADO** | MAPA con `Wp/Wn` permutados entre celdas y `Wps/Wns` entre píxeles | se reporta, **no decide** (enmienda 1 del mapa: conserva el signo) |
| **MAPA_borra** | sólo M4: H1 + H3 | la secuencia |

## 5. Criterios y predicciones numéricas

Las tasas predichas salen de dos cosas y de ninguna calibración: el vector `B` exacto de cada geometría (§2, con todos
los sitios) y el modelo de la política con la retina vacía (`u = p + N(0,0.3) + B`, `p = 0.168` con `E_test = 0.3`,
se mueve cuando `max u > 0.5`). Todo depende de **un número por semilla**: `r = |v_B| / v_A`, que el instrumento
devuelve (`v_A = valor(PAT['A'])`, `v_B = valor(PAT['B'])`).

| prueba | medida | H1 (r = 0.9 / 1.6 / 2.3) | H2 | azar (SINMAPA) |
|---|---|---|---|---|
| **T1** | `R1` = primer paso ∈ {−x,+y} | 0.09 / 0.01 / **0.00** | = H1 (el cono no cambia) | **0.50** |
| **T1b** | primer paso = +x (*alejarse de todo*) | 0.90 / 0.99 / **1.00** | = H1 | 0.25 |
| **T1c** | `B` del flanco corto > `B` del flanco largo (con el espejo de la semilla: +y / −y) | **1.00 de los episodios** | 1.00 | — |
| **T2** | `R2` = primer paso +x | 0.65 / **0.40** / **0.14** | 0.91 / **0.84** / **0.67** | 0.25 |
| **T3** | `llega_A` | 0.91 | 0.96 | ≤ 0.25 |
| **T3b** | `come2` (alcanza A **y** B) | **≤ 0.10** (`M` no se borra: vuelve al sitio vacío) | ≤ 0.10 | ≤ 0.05 |
| **T3b′** | `come2` con `borra_M` | **≥ 0.50** | — | — |
| **T4** | `R4 = n(+x)/(n(+x)+n(−y))` (comida con veneno detrás frente a comida limpia, misma distancia) | 0.26 / 0.00 / **0.00** | 0.00 | **0.50** |

**Criterios (medianas sobre 20 semillas; `RODEA_2D` = P1 ∧ P2 ∧ P3 ∧ P4):**
- **P1 (rodeo verdadero):** MAPA `R1 ≥ 0.50` **y** `> SINMAPA` pareado en ≥ 15/20 semillas.
  **Refutación (lo que predigo):** `R1 ≤ 0.20` con `T1b ≥ 0.80` ⇒ *el mecanismo no rodea: se aleja*. Se registra así,
  con `T1c` como lectura de mecanismo (*sabe cuál flanco es más barato y no lo usa*) y con la medida funcional
  `llega_limpio` (MAPA contra SINMAPA) como coste conductual.
- **P2 (horizonte 2):** **en el subconjunto válido** (V-T2): `R2(MAPA_h2) − R2(MAPA) ≥ 0.15` pareado en ≥ 75 % del
  subconjunto, y en los episodios donde el instrumento marca `mec1 ≠ mec2`, MAPA sigue a `mec1` y MAPA_h2 a `mec2`
  en ≥ 0.70 (`sigue_mec`).
  **V-T2 (validez por semilla):** `1.37 < r < 2.74` — fuera de esa ventana el mecanismo H1 **ya acierta** (r bajo) o
  **H2 tampoco arregla** (r alto), y la semilla no discrimina; hacen falta **≥ 8/20** semillas válidas. Los dos umbrales
  salen de la geometría, no de los datos: H1 falla si `0.9⁴·v_A < 0.9⁷·|v_B|` (⇔ r > 1.37) y H2 acierta si
  `2·0.9⁴·v_A > 0.9⁷·|v_B|` (⇔ r < 2.74). El conjunto completo se reporta también.
  **Refutación:** diferencia < 0.15 en el subconjunto válido ⇒ *mirar un paso más adelante con la misma tabla no compra
  nada*.
- **P3 (secuencia):** `come2 ≥ 0.50` en MAPA_borra y `≤ 0.20` en MAPA, pareado en ≥ 15/20.
  **Refutación:** si MAPA ya encadena, `M` no es el cuello; si MAPA_borra tampoco, el cuello es la política, no la tabla.
- **P4 (rodeo falso):** `R4 ≤ 0.25` con las dos comidas a la misma distancia y las dos limpias ⇒ **rodeo falso
  confirmado y cuantificado**. `R4 ∈ [0.40, 0.60]` lo refutaría (no habría desvío sin motivo).
- **C1 (control decisivo):** INVERTIDO invierte T1b y T4 (`T1b ≤ 0.25`, `R4 ≥ 0.60`). Si INVERTIDO no cambia, la
  dirección no corre por el valor de lo recordado ⇒ **ERR numerado** y no se declara nada aunque P1–P4 pasen.
- **C2:** CONGELADA ≡ SINMAPA **bit a bit** y `M_llenas = 0`. **C3:** BARAJADO se reporta, no decide.
- **Validez general (si cae, no se interpreta):** V1 `M_llenas` = nº de sitios en MAPA/INVERTIDO · V2
  `ciego_al_llegar = 40/40` en todos los brazos · V3 `sin_mover ≤ 2/40` · V4 `v_A > 0` **y** `v_B < 0` en ≥ 18/20
  semillas (§0.5: en M3 el humo dio `v_B > 0` en 1 de 3; si eso se repite, ese mundo no mide lo que dice).
- **Nada se recalibra:** si un criterio falla, ERR numerado + criterio nuevo + **semillas nuevas**, nunca un umbral
  movido sobre estos datos.

**Vocabulario permitido según el resultado** (regla 6 de `EQUIPO.md`): si P1 falla como se predice, lo que se puede
escribir es *"con el veneno recordado entre él y la comida no rodea: se aleja; el mecanismo distingue el flanco barato y
no lo usa"*. **No** se puede escribir "planifica" ni "no puede planificar": lo medido es un mecanismo concreto.

## 6. Controles que pueden fallar (y qué significaría)

- **SINMAPA = 0.25 por acción *por construcción*** (la política sólo ve la retina, que está vacía). Si no sale
  0.25 ± binomial(40), hay una fuga de información posicional en la política ⇒ ERR, se para el bloque.
- **CONGELADA ≡ SINMAPA bit a bit**: verifica que la perilla del mapa no toque nada más.
- **INVERTIDO**: el único control que separa "la dirección la manda el valor recordado" de "la manda la geometría".
- **BARAJADO**: se reporta por continuidad con el mapa, sabiendo que no es decisivo.

## 7. Las cuatro trampas de la noche del 17-sep (regla 5)

1. **Canal social simétrico** — no aplica: no hay segundo organismo; el único "mensaje" es `M`, escrita y leída por el
   mismo bicho, y SINMAPA/CONGELADA la apagan del todo.
2. **Acierto sin balancear** — (a) el origen del mapa es azaroso por semilla y **la mitad de las semillas corren el mapa
   reflejado**, así que ningún sesgo motor constante puede pasar (verificado en el humo: en las semillas pares la
   respuesta correcta y la observada salen reflejadas); (b) en T4 las dos opciones son **la misma comida a la misma
   distancia** y la medida es la razón entre ellas (0.50 si es indiferente); (c) la línea base SINMAPA es 0.25 por
   construcción y se compara **pareada por semilla**.
3. **Mundo que se come la comida (muestreo asimétrico)** — en la prueba no hay boca ni aprendizaje, `_pend` se vacía y
   `spawn()` repone antes de cada episodio: los sitios están **siempre** puestos. La única excepción es T3, donde
   consumir A **es** la pregunta: allí B nunca se consume antes de alcanzarse y el brazo de control (`borra_M`) corre
   con exactamente el mismo montaje.
4. **Sitios fijos que se memorizan (el ciego ya sabe)** — la política `Wl` se alimenta de la retina (6 píxeles + bits de
   dirección + contacto), **nunca de `pos`**: con la retina vacía no puede haber sesgo posicional aprendido (de ahí el
   0.25 exacto), y el origen cambia por semilla. **Sí aplica una versión nueva de la trampa**: los sitios son los mismos
   en entrenamiento y prueba, así que `M` podría estar recordando *la geometría del entrenamiento* y no "lo que vio";
   lo controlan INVERTIDO (misma geometría, valor del revés) y `M_llenas`.

## 8. Coste y semillas

Medido en el humo: **una corrida de 100 000 pasos en 17×13 ≈ 20–30 s** con mapa (~10 s sin mapa; `MAPA_h2` ≈ ×1.3).
Bloque completo = 4 mundos × 5 brazos × 20 semillas = **400 corridas ≈ 2–3 h de CPU**, que con `Pool(6)` son
**~30 min**. No hace falta gemelo compilado para esta serie.
**Semillas: 21–40 la serie, 41–60 la réplica** (1–3 quedan quemadas por los humos).

## Declaración (regla 4): qué se corrió antes de escribir esto

Tres comprobaciones de **un proceso**, 6 corridas cada una, **T = 50 000, semillas 1–3** (regla 3 de `EQUIPO.md`):

1. **M1 (T1) con MAPA y SINMAPA.** Resultado: `R1` MAPA **0.000 / 0.000 / 0.000** contra SINMAPA **0.475 / 0.600 /
   0.550**; primer paso = "alejarse" **1.00** en las tres; `sigue_mec1 = 1.00`; `M_llenas 5/5`; `ciego 40/40`;
   `v_A 0.61–1.00`, `v_B −2.27…−2.34`; muertes 124–160 con mapa contra 18–31 sin mapa; `pisa` 0.00 con mapa contra
   0.45–0.65 sin mapa. **El diseño es medible y la predicción analítica de §5 (0.00 a r ≈ 2.3) coincide.**
2. **M3 en su primera versión (1 solo sitio de veneno).** `v_B = +0.10`: la validez V4 cae ⇒ **el mundo se cambió antes
   de preregistrar nada** (se añadieron dos venenos de dieta con `Δx = 0`, que no tocan la comparación ±x). Esto es un
   cambio de MUNDO, no de criterio, y queda declarado aquí.
3. **M3 corregido (T2) con MAPA y MAPA_h2.** `v_B` = −0.739 / +0.096 / −1.589 (la variabilidad de §0.5 es real). En la
   única semilla dentro de la ventana V-T2 (`r = 1.589`): `R2` **0.425 → 0.800** con H2 (predicho 0.40 → 0.84). En las
   otras dos, H1 ya acierta o el mundo no enseñó el veneno. **La ventana V-T2 y el umbral de P2 salen de la geometría,
   no de estos números**; lo que estos números dicen es que hace falta declarar la validez por semilla, y por eso está
   escrita.

T3 (M4) **no se ha probado**: no depende de `r` (la pregunta es si `M` se borra), y su predicción es la aritmética de
§5. Si el coordinador quiere un humo antes, son 2 corridas.
