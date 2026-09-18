# DISEÑO — MUNDO VIVO (nivel 11): dos necesidades, cuatro estímulos

Diseñador, 18 sep 2026. Encargo: línea **(F)** de `registro/PLAN.md` (director, 06:10). Nada corrido con `Pool`.
Entregables en `experimentos/nivel11_mundo_vivo/`: `construye_vivo.py` → `organismo_vivo.py` · `identidad_vivo.py`
(**37/37**) · `mini_vivo.py` + `mini_vivo_salida.json` · `PREREGISTRO_mundo_vivo.md` (borrador para el coordinador).

## 1. El diseño en una frase

El cuerpo pasa de un escalar a un vector: **energía y agua**, cada uno con su descenso y **su muerte**. El mundo pasa
de dos estímulos a **cuatro**, que son **los cuatro patrones que ya existen** (A comida +0.8 E, B veneno −0.4 E,
C agua +0.8 Ag, D sal −0.4 Ag): un `+` y un `−` por eje, la cuarteta mínima que completa la tabla. La mordida deja de
tener una consecuencia y pasa a tener **un vector** `ΔS = (ΔE, ΔAg)`, con el mismo mapa de recompensa del tronco
(`ΔS_n > 0 → +1`, `< 0 → −3`, `= 0 → 0`). La boca decide con la **necesidad activa** (la de mayor déficit): lee *su*
fila de valor y usa *su* déficit como impulso. El valor se aprende **por estímulo y por necesidad**: `Wp/Wn` y
`Wps/Wns` pasan de vector a matriz `(n_nec, ·)`. El predictor de `ΔE` del bloque 6 pasa a **vector** y da una
**sorpresa por necesidad** (inerte por defecto; es la dosis de v15 hecha específica). Comprobado que vive y se
comporta como el del bloque 6, ahora por eje: sorpresa [0.095, 0.086] a T = 300 → [0.013, 0.020] a 3000 → [0, 0] en
régimen, y vuelve a subir en el eje que cambia si se cambia la tabla del mundo.

**Por qué el valor debe ser por necesidad y no un escalar con la necesidad como contexto.** Porque la consecuencia es
un vector: el error es un vector y un escalar por celda **no tiene dónde poner** la componente de la necesidad que no
está activa. Es la predicción que separa el diseño de su alternativa, y está medida: con un solo escalar (`val_esc=1`)
el valor del agua queda en **+0.43** y el de la comida en **+0.15** — *la memoria promedia lo que el mundo separa* — y
al organismo **le va peor que si no tuviera la segunda necesidad** (160 contra 141 muertes). La tercera vía, el
**código conjuntivo** (la necesidad como dos píxeles más de la retina), se descarta con razón medida: cambiaría `KW`
de (90, 6) a (90, 8) y con ello el consumo del rng desde el primer paso — **rompe el ancla** — y además duplicaría los
códigos por estímulo sobre un pool de 90 celdas que ya es el techo medido de la composición. El valor por necesidad
cuesta memoria (`n_nec ×` los pesos) y **cero celdas**. Queda escrito como brazo `nec_retina`, no construido.

## 2. Ancla de identidad: alcanzada, y en su forma fuerte

**Con una necesidad y dos estímulos el mundo vivo es `organismo_v14` bit a bit**, mismo consumo del rng y **mismas
claves de salida**. `identidad_vivo.py`: **37/37** (12 casos, 3 semillas, T = 20000, un proceso). Casos (I) y (J) son
la lectura literal del encargo: **toda la maquinaria encendida** (`vivo=1`: consecuencia vectorial, dos muertes,
drenaje de agua, contadores) con una necesidad y dos estímulos → todas las claves de v14 idénticas; lo único que
aparece son 10 claves nuevas de sólo lectura. Con `vivo=0` el conjunto de claves es **literalmente el de v14**.
Caso (M) es el control que **debe fallar** y falla (4 estímulos y 2 necesidades ≠ v14): sin él el arnés pasaría por
vacuidad. Cómo se consigue: ninguna línea nueva toca el rng del organismo (el único `Generator` nuevo es propio,
`seed+900000`, y sólo se crea con la perilla encendida); el único sorteo sensible al mundo es
`spawn(): rng.integers(len(tipos))`, y **por eso los cuatro estímulos son los cuatro patrones que ya existen** — no
cambia la retina, ni `KW`, ni el bucle de rechazo de `cond()`; el eje de energía **es** el de v14 por construcción; la
segunda muerte es imposible sin drenaje; y `Wp[0]` sobre la matriz es la misma vista 1-D, los mismos dobles IEEE.
*El tronco se movió a v14.1 (`eta_s` 0.15, `clip_s` 10) a las 05:55 mientras se construía esto: el `sha` abortó el
constructor, el instrumento se reconstruyó por anclas contra v14.1 y el arnés se repitió entero.*

## 3. Mini-prueba (3 semillas, T = 100000, un proceso; predicciones escritas antes)

| brazo | `xor01` | `exp_tabla` (celdas) | muertes [energía, agua] |
|---|---|---|---|
| **VIVO** (2 necesidades, 4 estímulos) | **1.00** (3/3) | **9** (4/4) | **89** [52, 37] |
| UNA_NEC (mismo cuerpo, una necesidad en la mente) | 0.50 | — (2/4) | 141 [52, **97**] |
| ESCALAR (`val_esc=1`) | 0.50 | — (2/4) | 160 [66, 94] |
| BARAJA_POL (`nec_shuf=1`) | 1.00 | 7 (4/4) | **361** [188, 181] |
| BARAJA_CON (`nec_shuf=2`) | **0.25** | 9 (4/4, transitorias) | 175 [86, 89] |
| NO_INFORMA (sal muda) | 1.00 | — (la sal nunca cruza) | 34 [33, **0**] |

**(a) Exposiciones.** VIVO aprende la tabla **2 × 4 completa** en 7 / 2 / 9 / 3 exposiciones (hambre×comida,
hambre×veneno, sed×agua, sed×sal) y la deja exacta: hambre {A +1.0, B −3.0, C 0.0, D 0.0}, sed {A 0.0, B 0.0,
C +1.0, D −3.0}, idéntica en las tres semillas. **Un encuentro sí informa a las dos necesidades**: las celdas cruzadas
("la comida no quita la sed") se aprenden sin una sola mordida dedicada. **Coste medido, no predicho:** hambre×comida
tarda 7 exposiciones en VIVO contra 4 en UNA_NEC — interferencia real de los `R = 0` que el agua y la sal escriben en
la fila de hambre por los píxeles compartidos de la vía lenta.

**(b) El XOR natural.** La tabla de "¿vale la pena morder?" sobre {hambre, sed} × {comida, agua} es (1, 0, 0, 1):
**paridad**, no representable como `a_necesidad + b_estímulo`. VIVO da `xor01` = 1.00 (3/3); ESCALAR 0.50;
BARAJA_CON 0.25 (bajo el azar). **El organismo no aprende el XOR: lo disuelve**, porque el término de interacción
está en la *memoria* (indexada por la necesidad) y no en el *lector*. Esto no reabre el XOR de píxeles de la línea 3
—ése sigue cerrado por dinámica— pero dice algo que vale para ese frente: *cuando la variable que hace el XOR es un
estado del cuerpo, indexar la memoria por ella es más barato que aprenderlo*.

**(c) Supervivencia.** Con dos muertes posibles, VIVO muere 89 veces; el mismo cuerpo con **una** necesidad en la
mente muere 141, **2.6 × más de sed** (97 contra 37). La segunda necesidad se paga sola.

**Lo que falló, y era mío.** (1) **El control "necesidades barajadas" estaba mal escrito** (MP-3 refutada): barajar
*qué necesidad cree la boca que está activa* **no** destruye la tabla —cada fila sigue recibiendo su componente— y
`xor01` se queda en 1.00; lo que destruye es la conducta (361 muertes). El control que el diseño necesita baraja **el
contenido** (qué componente de `ΔS` enseña a cada necesidad): con él `xor01` cae a 0.25. Instrumento corregido (dos
modos, dos lecturas distintas), arnés repetido, **37/37**. (2) **La predicción conductual P4 (contraste de tasa de
mordida ≥ 0.15) está refutada: 0.07.** El organismo muerde casi todo (tasas 0.90–1.00) porque
`Vb = α·W + 2·déficit + 0.5`: **un valor de cero no puede vetar a la boca de v14, sólo uno negativo la frena.** Es un
fallo de *política*, no de aprendizaje (regla 4), y era exactamente la trampa nueva que el preregistro declaró. La
conducta del mundo vivo hay que medirla donde sí manda: en supervivencia. (3) **La trampa 3 confirmada y peor de lo
acotado**: el veneno se encuentra 6.3 × más que la comida (5253 contra 831) porque lo rechazado se queda y lo mordido
desaparece; `exp_hasta` es inmune (cuenta exposiciones a *ese* estímulo), pero ninguna medida agregada sobre estímulos
puede entrar al bloque. (4) **La primera cruzada puede ser transitoria**: BARAJA_CON "cruza" las cuatro celdas y
termina en puré → una celda sólo cuenta si además **termina** con el signo correcto. Las cuatro van como ERR
candidatos (el último del registro es ERR-32) en la Enmienda 1 del preregistro, escrita antes de la serie de 20.

## 4. Propósito y reproducción

**Primero como medida, sin construir nada.** `descendientes_viables = ⌊∫ max(E − 1.0, 0) dt / C_hijo⌋` con
`C_hijo = 100000 × (costo + costo_a) = 200`: el **excedente sobre la saciedad**, no la energía total. Es un contador
de sólo lectura (una línea, no toca el rng) que resume en una cifra supervivencia, aprendizaje y las dos necesidades.
Predicción ya escrita: VIVO > UNA_NEC > BARAJA_POL, en el mismo orden que la supervivencia; si se invierte, la medida
no mide lo que dice y se tira. **Después como mecanismo**, cuando la medida esté replicada: al pasar de 1 a 2, nace
una copia que hereda `KW`, `activa` y las filas de valor con `olvido_hijo` (la perilla ya medida de la Etapa 4), en su
propio anillo, y el padre paga `C_hijo`. Sólo entonces se mide el criterio de emergencia del punto 14 del brief y si
la **selección sobre el organismo entero** encuentra lo que el diseño no encontró — la salida que el director dejó
escrita en el criterio de parada del 04:55. No se construye ahora: exige población y `Pool`.

## 5. Recomendación honesta

**Sí vale correr el bloque completo, pero no es el frente único.** Lo que el mundo vivo demuestra en 3 semillas es
grande y limpio (tabla 2 × 4 exacta en ≤ 9 exposiciones, `xor01` 1.00 contra 0.50 del escalar y 0.25 del barajado,
supervivencia 89 contra 141/160/361) y **es barato**: el bloque son 6 brazos × 20 semillas sobre un instrumento con
identidad 37/37, sin `Pool` nuevo que inventar. Lo que **no** demuestra es que esto acerque a la AGI por sí solo: el
mundo vivo **compra estructura, no regla** — resuelve el XOR necesidad × estímulo porque se lo da hecho en la forma
de la memoria, y el cuello del frente abierto (construir el rasgo conjuntivo a partir de píxeles, creador A, 18-sep)
sigue intacto. Su valor real para la misión es otro y conviene decirlo así: **da un criterio de éxito que no es un
acierto sino estar vivo**, y con dos necesidades el organismo por fin puede *equivocarse de objetivo*, que es la
condición mínima para que "propósito" signifique algo medible.

**Semillas:** el bloque en **181–200** (rango virgen; 161–180 lo usó el tercer examen de v14) y, por la regla 12, si
`xor01` o cualquier pareado queda a ±1 semilla del umbral, réplica automática en **201–220**. Antes de correr:
P4 sustituida por P4' (supervivencia), P3 desdoblada en P3a/P3b, P5 endurecida y P7 a 2 × — todo en la Enmienda 1, ya
escrita. **Orden sugerido:** correrlo *después* del bloque 2/3 del criterio de parada (aprender sin morder), no antes:
el criterio de parada del director tiene prioridad y este bloque no lo toca.

---

# APÉNDICE (18 sep, tras correr 181–200): qué nivel mide este mundo y cómo queda la ficha

## Resultado del bloque, en una línea

**Núcleo sostenido, supervivencia y sal no como se predijo.** P1 20/20 (`xor01` 1.0), P2 20/20, P3a 20/20,
P3b ×3.76 (18/20), P5 con la lectura aclarada, P9 4.0 = 4.0. P4′ y P7 caen **por cómo los escribí**, no por el
efecto: puse los umbrales pareados *en la mediana* del efecto (0.75 contra una mediana pareada de 0.739; 2 × contra
1.99), lo que parte la muestra por la mitad por construcción, mientras el efecto real es grande y consistente
(A₁₂ = 0.90 contra UNA_NEC, 0.935 contra ESCALAR, 0.955 en muertes por agua; q75 de VIVO por debajo de q25 de los
dos). P6 cae por un `max` sobre 40 lecturas cuando la mediana es 0.0 y 18/20 semillas dan 0.0 exacto. Los tres son
**ERR-37**, y la Enmienda 2 del preregistro los sustituye para 201–220 con margen declarado.

## Qué nivel del brief mide este mundo — respuesta honesta: **ninguno lo cierra; toca tres**

- **No es nivel 5.** Nivel 5 es transmisión entre organismos. Aquí hay uno solo: "significado por necesidad" no es
  comunicación, y llamarlo así sería vocabulario inflado (regla 6).
- **Nivel 8 (aprendizaje abierto) es su casa principal, en la columna "hecho".** Es el primer mundo del proyecto con
  más de una dimensión de valor: el estímulo deja de tener *un* valor y pasa a tener uno *por necesidad*, y el
  organismo aprende la tabla 2 × 4 completa en 2–11 exposiciones por casilla, exacta en 18/20 semillas. El aporte es
  mensurable y nuevo, pero **no mueve el porcentaje**: los cabos de esa fila (retención de lo ausente 0.67, canje del
  mapa cerrado, dominio distinto del anillo) siguen intactos. **8 sigue en 40 %.**
- **Nivel 9 (autonomía) es donde más cambia, y ahí sí propongo mover el número.** La fila decía "allostasis (bloque
  6), meta propia" como lo que falta. La allostasis mínima ya está medida: dos necesidades que bajan solas, dos
  muertes posibles, y una política que elige *cuál manda* (la de mayor déficit). El organismo puede, por primera
  vez, **equivocarse de objetivo** — condición mínima para que "propósito" signifique algo medible — y se paga en
  supervivencia (A₁₂ 0.90 contra el mismo cuerpo con una sola necesidad en la mente). **Propuesta: 9 de 20 % → 30 %.**
- **Nivel 4 (memoria persistente) recibe un negativo nuevo y nítido**, que es el hallazgo más transferible del
  bloque: con cuatro estímulos, dos pueden compartir código (2.5 % de las semillas), y entonces la puerta por
  evidencia de código **presta** la evidencia de uno al otro, `div_signo` **no puede** repararlo cuando el estímulo
  mudo da `R = 0`, y la evitación cierra el bucle. **El precio lo paga el veneno: su valor cae de −3.00 a −1.83 /
  −1.34.** Es una grieta del tronco, no del mundo vivo: con dos estímulos `cond()` prohíbe el alias por
  construcción, así que v14 nunca fue puesto a prueba en esto. **4 sigue en 60 %**, con un cabo nuevo.
- **Nivel 3 (generalización) NO se toca.** El XOR necesidad × estímulo es paridad de verdad, pero se resuelve
  *indexando la memoria*, no leyendo mejor los píxeles: no es el XOR de la línea 3 y sumarlo allí sería inflar.

## Ficha para `HANDOFF.md` §13 (texto para pegar; los porcentajes son propuesta)

> | **4 memoria persistente** | *(sin cambios)* | … + **con 4 estímulos dos pueden compartir código (2.5 % de semillas medidas): la puerta por evidencia de código presta la evidencia del vecino, `div_signo` no puede dispararse con `R = 0` y la evitación cierra el bucle; el estímulo mudo le quita al veneno el 40–55 % de su valor (−3.00 → −1.83/−1.34). `PREREGISTRO_supersticion_sal.md`** | 60 % |
> | **8 aprendizaje abierto** | … + **mundo vivo (nivel 11, 181–200): dos necesidades y cuatro estímulos; el valor deja de ser un escalar y pasa a ser uno POR NECESIDAD; tabla 2 × 4 exacta en 18/20 semillas con 2–11 exposiciones por casilla; `xor01` necesidad × estímulo 1.00 (20/20) contra 0.50 del valor escalar (20/20) y 0.25 al barajar el contenido (20/20)** | … + **el contraste conductual por estímulo NO aparece (0.07): con `hambre_boca = 2.0` un valor de cero no puede vetar a la boca; sólo uno negativo la frena (fallo de política, no de aprendizaje)** | 40 % |
> | **(9 autonomía)** | recuperación medida ante cambio no avisado · **allostasis mínima MEDIDA: dos necesidades con su descenso y su muerte, la activa manda, y la segunda necesidad se paga sola en supervivencia (A₁₂ 0.90 contra el mismo cuerpo con una sola necesidad en la mente; muertes por agua 48 contra 89)** | meta propia; propósito y reproducción sólo como medida (`descendientes_viables`), sin mecanismo | **30 %** |

## Lo que yo haría ahora (recomendación, no decisión)

1. **Réplica 201–220 con la Enmienda 2**, que es barata (~4 min) y trae **P10**, la predicción que puede fallar
   limpiamente: 201–220 **no tiene ninguna semilla con alias de código** (calculado antes de correr con
   `diagnostico_codigos.py`), así que P6′ debe salir 20/20 y el peor error de casilla de VIVO **0.00 en 20/20**. Si
   aparece una semilla sucia sin alias, mi explicación de la superstición es falsa.
2. **El bloque de la sal, después y sólo si hay hueco**: es nivel 4, no nivel 11, y su coste hoy es el 2.5 % de las
   semillas. Lo que lo hace valioso no es el tamaño sino que **señala un órgano que falta**: una división que se
   dispare por conflicto de *información* (`R = 0` sobre una celda consolidada) y no sólo por conflicto de *signo*.
3. **Lo que NO haría:** declarar nivel 5 ni tocar el nivel 3. Y no arreglaría la política (el contraste conductual)
   metiendo un coste de mordida: sería un mecanismo nuevo para salvar una predicción mía que ya está refutada y
   sustituida por una medida mejor (supervivencia).
