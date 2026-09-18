# DIAGNÓSTICO — sala 2, lente MUNDO Y MEDIDA (18 sep 2026, ~09:45)

**Misión (primero):** llegar a la AGI por este camino — un organismo mínimo con reglas locales, sin backprop en el
runtime, que aprende, desaprende, generaliza, sobrevive y se reproduce con evidencia preregistrada. Primero llegar a la
frontera; segundo, que viva. **Lente de este diagnóstico:** el mundo (necesidades, valor por necesidad, cuello de botella
`min(E, Ag)`), la medida de reproducción que se tiró, y qué mundo y qué medida harían de "vive" un resultado y no una
metáfora. Nada aquí es un preregistro: es un diagnóstico con evidencia (archivo, entrada, número) para el coordinador y
el director. No edité ningún archivo del repo; no corrí nada (ni `Pool` ni un proceso): todos los números salen de los
registros, de los preregistros y de los JSON ya guardados en `datos/` (un cálculo nuevo, declarado en §2.1, se hizo
leyendo `datos/examen_v14_20260918_054720.json`, sin simular).

Fuentes leídas, en este orden: `CLAUDE.md` (bloque día 7), `registro/PLAN.md`, `registro/HANDOFF.md` §13 y §15.7–15.8,
`registro/REGISTRO_etapas_1_2.md` (ERR-35 → ERR-42), `registro/investigacion/ENJAMBRE_xor_20260918.md`,
`registro/investigacion/PUENTE_creacion.md` (A12–A16, B-4, B-5), `experimentos/creacion_A/PREREGISTRO_v15e.md`,
`experimentos/nivel11_mundo_vivo/PREREGISTRO_mundo_vivo.md`, `PREREGISTRO_reproduccion.md`, `PREREGISTRO_reproduccion_2.md`,
`registro/investigacion/DISENO_mundo_vivo_20260918.md`, `organismo/organismo_v14.py` (entero),
`experimentos/nivel11_mundo_vivo/organismo_vivo.py` y `organismo_vivo_rep2.py`, `registro/EQUIPO.md`,
`BRIEF_ORIGINAL_y_estado.md` (puntos 11–16), y los logs de `datos/v15e_s141-160_20260918_092921`,
`examen_v15e_20260918_093053`, `regresion_generaliza_v15e_…_093352`.

---

## 1. Dónde está exactamente la frontera hoy (con números)

| capa | estado al 18 sep 09:40 | evidencia |
|---|---|---|
| **Tronco** | **v14.1** (`organismo/organismo_v14.py` feefc88b1fd8d434): v13 + hija dispersa + puerta por código exacto, `eta_s` 0.15 / `clip_s` 10. Examen v3′ 8/8 en tres rangos, generalización 1.000 / 0.95, capacidad `N*` 51, 3T-k 0.237 | CLAUDE.md día 7; REGISTRO 05:05 y 06:05 |
| **Aprende / desaprende / generaliza** | Sí, lineal: E1/E2 20/20 (aprende e invierte), G1 1.000. No lineal: **línea XOR CERRADA 07:47** — con 8 ejemplos exige un prior de pares (M3: 1.000 / 1.000, n\* = 7–10 en dos series) y con 14 no hace falta (1.000, n\* = 200); con 8 y sin prior no lo aprende nadie (gradiente exacto 0.562, backprop 0.531, 9 de 15 hipótesis empatadas) | REGISTRO 07:43 y 07:47; PUENTE A12–A15 |
| **Candidatos a v15** | **Ninguno entra.** v15c (V1 medida apagada, ERR-38), v15d (E2 0/20: no se desdice; E1 0/20), **v15e (09:37): V1 19/20 (E1 `venenoQ4<Q1` 19/20; E2I `W_C ≤ −2.5` 19/20), V2b xor01 estricta 0.500 (OFF 0.438) → NO ENTRA** por §7. B-5 (desambiguar códigos): DECLARADO, candidato a v15, decide el director | `datos/v15e_s141-160_…` ETAPA 5/5; `examen_v15e_…log` líneas 18 y 22; REGISTRO 09:12 |
| **Mundo vivo (línea F)** | Núcleo replicado ×2 (181–200, 201–220): valor por necesidad resuelve el XOR necesidad × estímulo **1.0 en 20/20** (escalar 0.5; contenido barajado 0.25), tabla 2 × 4 exacta en ~11 exposiciones; muere menos (97 contra 135.5 / 152.5; A₁₂ 0.90 / 0.935; sed 1.85–2.05×); alias de código confirmado por predicción (P10) y **reparado** por B-5 (18/18: sal 1.45 → 0.0, veneno −1.45 → −3.0, evitación ×7 → ×1, muertes 75 → 41) | REGISTRO 07:58, 08:16, 08:20, 09:07, 09:12 |
| **Propósito y reproducción** | **Medida 1 TIRADA (ERR-40)**: `descendientes_viables` premia atracones (ESCALAR 36 y BARAJA_CON 39.5 ventanas contra VIVO 20, muriendo 149.5 / 159.5 contra 100; A₁₂ 0.007 / 0.0). La tercera necesidad **sobra** (CUELLO_MIN 65.5 > REP_SIN_COSTE 55; A₁₂ 0.146). **Medida 2 preregistrada, NO corrida** (`r = descendientes − muertes`, 261–280; humo 5/5: CUELLO_MIN r +3 / −2, VIVO −75 / −86, ESCALAR −126 / −172) | REGISTRO 09:16; `PREREGISTRO_reproduccion_2.md` §0, §4, §10 |
| **Población, herencia, selección** | **No existen.** Un cuerpo por corrida; la muerte no borra nada; el descendiente es un contador; "qué se hereda: NADA" por diseño; el único código de población es `experimentos/dia1_exploracion/poblacion2.py` (día 1, anterior a v6, pool compartido `KW` de la especie, sin muerte real) | `PREREGISTRO_reproduccion.md` §2; BRIEF punto 14: "ningún resultado colectivo aún" |

**La frontera, en una frase:** el organismo aprende, desaprende y generaliza lo lineal con reglas locales (v14.1), cruza XOR
sólo con un prior declarado o con 14 ejemplos, sabe qué vale cada cosa para cada necesidad (mundo vivo) — y **todavía no
puede ni morir ni nacer**: cada "vida" dura ~770 pasos en el tronco (129.5 muertes por 100 000, examen E1, n = 6) y
~1 030 en el mundo vivo (97 muertes), la memoria sobrevive a todas, y ninguna medida de reproducción ha sobrevivido a su
propio preregistro.

---

## 2. Qué nos BLOQUEA para salir de la frontera (ordenado por importancia)

### Bloqueo 1 — La muerte no es muerte: el organismo es inmortal en memoria y el renacer es un recurso

**Evidencia.** `organismo/organismo_v14.py`, línea del bucle: `if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))` —
al morir se conservan `Wp, Wn, KW, activa, Wps, Wns, ncod`; sólo se reponen energía (0.6) y sitio. El brief lo sabe desde
v4 (punto 11: "memoria intacta tras muerte del cuerpo"). En el mundo vivo (`organismo_vivo.py`) es igual con `Ag=.6`.
**Cuánto pesa, calculado hoy del JSON del examen (`datos/examen_v14_20260918_054720.json`, `bateria_v14.py 6`, T = 100 000,
`costo` 0.002 → drenaje 200 unidades):**

| etapa (n = 6) | muertes (mediana) | ingesta neta por mordidas `0.8·A − 0.4·B` | regalo del renacer `0.6 × muertes` | **fracción del presupuesto que viene de renacer** |
|---|---|---|---|---|
| E1 | 129.5 | 255.0 | 77.7 | **0.236** [0.217, 0.289] |
| E2 (inversión) | 132.0 | 95.0 | 79.2 | **0.457** [0.427, 0.544] |
| E2I | 166.5 | 195.4 | 99.9 | 0.347 |
| CTRL | 146.5 | 343.4 | 87.9 | 0.210 |

En el mundo vivo (drenaje 100 por eje, `costo` 0.001): VIVO 97 muertes [53.5 energía, 48 agua] → sólo las muertes por
energía regalan ≥ 0.6 × 53.5 = **32 unidades = ≥ 32 % del drenaje de energía**; ERR-40 lo formuló como mecanismo ("el
renacer regala 600 pasos de drenaje y un escape del anillo atascado") y el humo de rep2 lo midió: el regalo financia
**65–77 % de las ventanas de ESCALAR y 34–36 % de las de CUELLO_MIN** (`PREREGISTRO_reproduccion_2.md` §10).

**Por qué bloquea.** Con la muerte gratis y la memoria inmortal, "sobrevive" no puede ser un resultado: es un contador de
resets; y "se reproduce" tampoco (nada nace, nada muere). Es la razón de fondo por la que la medida 1 se tiró (un cuerpo que
muere más gana más ventanas) y por la que la medida 2 tuvo que restar muertes con tipo de cambio 1:1 para que morir no sume.
Ninguna contabilidad sobre un inmortal mide viabilidad; a lo sumo ordena brazos.

**Qué lo desbloquearía.** Un **mundo de población mínimo** (`mundo_vivo_pob.py`, hoy no construido; el propio preregistro lo
nombra como "el cambio de paradigma que el director dejó escrito"): N cuerpos, **la muerte borra al individuo** (su `KW`,
`activa` y `W` desaparecen), y el linaje persiste sólo por **herencia** — al cumplir una ventana con coste real, nace una copia
con `KW`, `activa` y las filas de valor con `olvido_hijo` (la perilla de la Etapa 4, ya medida: heredar el valor ahorra el
80 % del veneno inicial, 20/20). Ancla obligatoria: con N = 1 y muerte sin borrado ≡ `organismo_vivo` bit a bit.
**Coste:** un instrumento por anclas (1 día de diseñador), arnés, y `Pool` (§4). Sin él, los bloqueos 2 y 5 no se pueden
ni plantear.

### Bloqueo 2 — La medida de reproducción: dos intentos, ninguno mide reproducción

**Evidencia.** Medida 1 (`descendientes_viables`, ventana de 500 pasos saciado en las dos): P-R1 A₁₂(VIVO > ESCALAR) 0.007 y
A₁₂(VIVO > BARAJA_CON) 0.0 → **se tira** (REGISTRO 09:16; ERR-40). Medida 2 (`r = descendientes − muertes`,
`PREREGISTRO_reproduccion_2.md` §1): elegida **mirando el dato** (declarado en §5, "elegir la medida mirando el dato: se
hizo"), con retrodicción sobre 221–240 (VIVO −80, CUELLO_MIN −13, 5/20 con r ≥ 0) y humo 5/5; **no ha corrido** (261–280).
Y por construcción (§2 "Qué se hereda: NADA"): el descendiente **se cuenta, no se instancia**.

**Por qué bloquea.** `r` es contabilidad de poblaciones aplicada a un solo cuerpo inmortal: "r ≥ 0 = tasa de reemplazo" no
significa reemplazo de nadie. Además está dominada por las muertes (~100) frente a los nacimientos (~20): el propio
preregistro lo declara como trampa propia (i) y tiene que apuntalarla con P2-3 y P2-5. El bloque puede pasar P2-1…P2-8 y
seguir sin haber medido reproducción; el vocabulario del §6 lo reconoce ("nada nace").

**Qué lo desbloquearía.** Que la medida sea la del bloqueo 1: **descendientes reales que sobreviven ≥ X pasos con memoria
heredada** (R₀ del linaje), **tiempo hasta la extinción del linaje** y el criterio de emergencia del punto 14 del brief
(propiedad ausente en el individuo, presente en el grupo, no programada, reproducible, que desaparece al romper la
estructura — hoy "ningún resultado colectivo aún"). Cláusula de validez heredada de P-R1: la medida debe ordenar como la
supervivencia (A₁₂ ≥ 0.70 en los pares ya medidos) o se tira por tercera vez. Control que puede ganar: **herencia barajada**
(el hijo hereda la memoria de otro linaje). **Coste:** cero código extra sobre el bloqueo 1; un preregistro.

### Bloqueo 3 — El mundo es adversario a la herencia por parecido y se come la comida

**Evidencia.** (a) Cuatro patrones de peso 3 sobre 6 píxeles: el **único** par lo bastante parecido para heredar es
comida/veneno (sim 0.225) — heredar por parecido **cuesta** (8 → 11 / 13 exposiciones) más de lo que gana donde el parecido
es débil (16 → 13); el código Kenyon `K = 3` de 90 **no ordena vecinos** (similitud 0.000 / 0.000 / 0.333 para 0 / 1 / 2
píxeles compartidos, contra 0.025 / 0.075 / 0.225 graduada en HD `nh = 2000, kh = 40`) (PUENTE B-4). (b) **Alias de código:**
con 4 estímulos algún par comparte código en 18/200 semillas (9 %); en el mundo de regla 170/200, y 135/200 tienen fuga px0
(PUENTE B-5, `negativo_codigo.py`). (c) **Trampa 3 confirmada y peor de lo acotado:** lo mordido desaparece y lo rechazado se
queda — el veneno se encuentra 6.3× más que la comida en la mini (5 253 contra 831), **23× en el ancla V14 del bloque**
(exposiciones B 7 897.5 contra A 344.5, `datos/vivo_s181-200`), y una semilla ALIAS visita la sal 3 835 veces contra 545
(bloque de la sal). (d) Refuerzo sólo al morder: 5 740 encuentros con veneno por corrida sin aprender nada (PLAN 04:55);
C-P5 (aprender sin morder por predicción) refutado.

**Por qué bloquea.** Es exactamente el mundo en el que la hipótesis del director ("sal rosa hereda de sal") **no puede**
medirse: no hay familias de estímulos, el parecido contradice el valor, y la señal que enseñaría a una arista (acierto o
fallo de la herencia) "es más rara que el problema que debe arreglar" (B-4). Y un mundo que se llena de lo rechazado
convierte cualquier medida agregada en muestreo (por eso todo va "por exposición").

**Qué lo desbloquearía.** Un mundo con **familias**: retina mayor (p. ej. 12 px) con patrones base y variantes que comparten
la **misma consecuencia `ΔS`** (eso, no los píxeles, es "ser lo mismo" para el cuerpo), más excepciones raras; **renovación
simétrica** (lo rechazado también desaparece a una tasa comparable, o se consume con el tiempo); código de alta dimensión
como soporte de aristas legibles (B-4 ya midió que hace falta). Medida: **exposiciones hasta asociar la variante** contra un
patrón nuevo no emparentado, y **tasa de herencia falsa** en las excepciones. Ancla: con 6 px y 4 patrones ≡ `organismo_vivo`.
**Coste:** un instrumento por anclas y un bloque; rompe el ancla del rng si se toca `KW` (el diseño del mundo vivo ya
documentó cómo evitarlo: generador propio `seed+700000`).

### Bloqueo 4 — Un valor de cero no veta y el impulso tapa el valor: el "propósito" es una lectura, no una conducta

**Evidencia.** `Vb = α·W + 2·déficit + 0.5`: con `W = 0` y déficit 0, `pb = 0.841`; saciado, VIVO **muerde la sal el 80 %
de las veces** (`sac_tasa[D]` 0.797) y se bebe la reserva; el contraste conductual por estímulo salió 0.07 (P4 refutada,
enmienda 1 del mundo vivo: "el impulso tapa el valor cero"). Lo que "arregla" eso es CUELLO_MIN — leer el mínimo de las dos
filas saciado (0.001) — un **enrutamiento de lectura**, sin aprendizaje, y la tercera necesidad no aporta sobre él (A₁₂
0.146). Es decir: hoy el único "propósito" medible cambia **una** conducta (no morder sal saciado) y ni siquiera exige memoria.

**Por qué bloquea.** Mientras la política no pueda decir "no" a un valor nulo, el mundo vivo sólo se mide en supervivencia y
no en conducta; y toda mejora de "propósito" se reducirá a parches de lectura. La regla 4 del proyecto lo exige separar:
es un fallo de política, no de aprendizaje, y nadie lo ha atacado con preregistro (el diseñador lo dejó escrito como
candidato `c_boca` y decidió, con razón, no meterlo para salvar una predicción caída).

**Qué lo desbloquearía.** Un bloque barato: **coste de la mordida inútil** (`c_boca`: morder cuesta E o Ag, como en biología
masticar cuesta) o una boca que lea **ΔS esperado** en vez de R (el predictor vectorial del bloque 6 ya existe, `eta_pred`,
inerte por defecto). Control: la conducta saciado y las muertes deben cambiar en la dirección predicha sin tocar `xor01`.
**Coste:** un preregistro y ~140 corridas.

### Bloqueo 5 — Sin población no hay señal que no sea la propia mordida, ni nada que transmitir

**Evidencia.** N2 (significado emergente) **cerrado con dos mundos** tras 6 diseños (contraste ±0.3, sin beneficio; INNATO 60
contra 278: el canal sirve **con significado dado**); N3d transfiere por conducta ajena (0.822 / 0.811 / 0.811) pero "mudo =
obedece, no enseña" (0.503) y crea dependencia (189 muertes); C-P6 nulo (el receptor aprende solo, SOLO_R 0.986). N1: el
novato aprende B con 7–8 mordidas en vez de 19 mirando al experto (20/20). Todo esto son parejas montadas a mano, no una
población que viva junta.

**Por qué bloquea.** "Aprender sin morder" y "lenguaje" (la hipótesis del director) necesitan un otro cuya consecuencia sea
visible y honesta; hoy el organismo sólo tiene su propia `R` (`R` sólo dentro de `if mordio:`). En población, la señal de
N1 (conducta visible + / −) es **honesta por construcción** y el `ΔS` del otro es la única fuente de información gratis que
el método ya validó.

**Qué lo desbloquearía.** El mismo mundo del bloqueo 1 con la señal de N1 (ya medida) como canal por defecto; medida:
exposiciones hasta asociar **con** un congénere visible contra **sin**; control: congénere barajado (ya validado como
destructivo en N1). **Coste:** cero mecanismo nuevo; entra con el bloqueo 1.

**Observación fuera de lente, para el coordinador (candidato a ERR, no cambia el veredicto de v15e):** en
`datos/v15e_s141-160_20260918_092921.log` la línea de umbrales imprime `V2a G1 1.000 >= .80 (azar 20.000) · G2 0.997 >= .85
(azar 20.000) · K 20.0/20  NO` mientras la batería (`regresion_generaliza_v15e_…_093352.log`) da `PASA G1 … PASA G2 … CONSERVA`:
el runner parece leer un conteo donde esperaba la mediana de `azar`. v15e cae igual por V1 y V2b.

---

## 3. Qué mundo y qué medida harían de "vive" un resultado (si fuera mi creación)

Lo digo con las piezas que ya existen, en el orden en que las preregistraría, y con lo que exige de `Pool`.

1. **Población con muerte real y herencia (bloqueo 1).** N cuerpos (N = 8) en un anillo compartido de `L = 40·N` casillas con
   `nobj = 4·N` (la misma densidad de hoy: un objeto por 10 casillas y cuatro por cuerpo), cada uno con su `KW`, `activa`,
   filas de valor y `ncod`. **Muerte:** el cuerpo desaparece con su memoria. **Nacimiento:** cuando un cuerpo completa una ventana de
   viabilidad **pagando** `rep_coste` (0.4 / 0.4, la moneda de daño que ya existe) nace una copia con `olvido_hijo` ∈ {0, 0.05}
   (los dos brazos de la Etapa 4) en una casilla vecina. **Selección:** ninguna programada — sólo la física. Ancla dura:
   `N = 1, muerte_borra = 0` ≡ `organismo_vivo` bit a bit (mismo rng: los cuerpos nuevos usan `seed + 1000·i`).
2. **Medida:** `linaje(t)` = número de cuerpos vivos; **tiempo hasta extinción** (censurado en T) y **R₀** = descendientes por
   vida que sobreviven ≥ 500 pasos. Cláusula de validez (la de P-R1): en los brazos ya medidos debe ordenar como la
   supervivencia (A₁₂ ≥ 0.70 VIVO > UNA_NEC > BARAJA_POL) o se tira. Umbral con significado y sin ajuste: **el linaje sobrevive
   a T = 100 000 en ≥ 15/20 semillas con `olvido_hijo = 0`, y en < 5/20 con herencia barajada** (el hijo recibe la memoria de
   un cuerpo de otra semilla). Si la herencia barajada no lo mata, lo que sostiene el linaje no es lo aprendido.
3. **Herencia como transmisión (nivel 5 sin canal):** brazo "hijo en blanco" contra "hijo con memoria": la diferencia en
   `R₀` es el primer número de transmisión medido en población, sin símbolo.
4. **Después (no antes): la tercera necesidad vuelve como PRUEBA, no como órgano.** En un mundo con muerte real, "saciado
   rechaza lo que daña al recurso escaso" (CUELLO_MIN) puede volver a ganar o no; lo que hoy es una lectura pasa a ser un
   rasgo heredable que la selección puede conservar o perder. Ahí sí "propósito" empieza a significar algo medible.
5. **Qué exige del `Pool`.** `organismo_vivo` corre a 5–9 s por 100 000 pasos; N = 8 cuerpos ≈ 40–70 s por corrida; 6 brazos
   × 20 semillas = 120 corridas ≈ 8–10 min con `Pool(14)`. Sin gemelo compilado (ningún instrumento del mundo vivo lo tiene;
   el tronco sí, `organismo_v14_rapido.py`): si el bloque se replica o se barre N, el gemelo del mundo de población es la
   herramienta que hay que pagar primero (regla 9 de EQUIPO). Regla 11: un `Pool` a la vez.

---

## 4. La hipótesis del director, desde esta lente

**Texto (09:40):** "si sal es sal será número uno, lo guardo, lo vectoriza; después sal rosa lo vectoriza, marca como sal y lo
plantea como una variable de lo mismo — eso es lenguaje; y ya lo hemos visto, que puede aprender y desaprender". Contexto
05:10: "la palabra es grafo, no vectorización".

### 4.1 Qué ya hace el organismo

- **Tokeniza.** El "número uno" existe: el código Kenyon exacto (3 celdas de 90, `code(P)`), y desde v14 hay un **registro de
  tokens** — `ncod` (dict código exacto → mordidas) y `_ord` (orden de aparición) — que la puerta usa para decidir si un
  patrón "le es familiar" (≥ 5 mordidas y ≥ 1 celda consolidada). Eso es una tabla de nodos sin aristas.
- **Vectoriza.** El valor del token es `(Wp − Wn)@código` (un escalar en el tronco) y en el mundo vivo **un vector por
  necesidad** (`Wp[n]`, matriz `(n_nec, 90)`): el mismo token vale +1 para el hambre y 0 para la sed. Esto es lo más cercano a
  "vectorizar el significado", y está medido (tabla 2 × 4 exacta, 20/20 ×2).
- **"Sal rosa marca como sal": lo hace, y es su enfermedad medida.** Cuando dos estímulos comparten celdas, el valor se
  presta por las celdas compartidas: fue la **generalización de v9 = su interferencia** (fuga 1 de cada 3 celdas), v11 la
  tapó (0.08) y perdió la generalización (0.60), v13 la recuperó por otra vía (la lenta lineal). Y en su forma extrema
  (mismo código), **la sal "es" el veneno**: |W[sal]| 1.45, veneno −1.45 (bloque de la sal, 9/9). El organismo ya trata "sal
  rosa" como "variable de lo mismo" — sin poder separarlas.
- **Separa la variable cuando el mundo la desmiente.** La división por conflicto de signo (v11) y, desde hoy, la **división
  por `R = 0` bajo retina distinta** (B-5): "cuando una celda con valor recibe nada bajo una retina distinta, divide: el
  código deja de prestar valor" (sal 0.0, veneno −3.0, 18/18). Eso es exactamente "sal rosa deja de ser sal cuando no hace lo
  que sal hacía": la operación de desligar existe y es local.
- **Aprende y desaprende.** E1/E2 20/20 en el tronco; lo que no se desdice es la memoria de un golpe (v15d E2 0/20), y lo que
  se desdice pierde el prior (v15e xor01 0.500). El canje "exacto a la primera / se desdice en una / cruza XOR" está medido
  y no resuelto.

### 4.2 Qué no hace

- **No tiene aristas.** No hay una relación explícita entre tokens: ni "sal rosa → sal" ni "sal ≠ veneno". La única relación
  es implícita (celdas compartidas), y ésa **no ordena vecinos** (K = 3: 0.000 / 0.000 / 0.333) — B-4 midió que para tener
  aristas de parecido legibles hace falta el soporte de alta dimensión (HD 2000/40), que el director aceptó "sólo como
  soporte del grafo".
- **Heredar por la arista no acelera en este mundo:** exposiciones hasta asociar 16 (v14) → 13 con la vía lenta, y **empeora**
  (8 → 11 / 13) cuando el parecido engaña; la fiabilidad de la arista aprende demasiado tarde (2–3 episodios por patrón).
  No es que el grafo esté mal: es que el mundo no tiene familias (bloqueo 3).
- **No es lenguaje.** Lenguaje exige que el token viaje entre organismos con significado: N2 falló seis veces por refuerzo
  (contraste ±0.3) y sólo funciona con significado dado (INNATO). La transmisión que sí existe (N1, N3d) es por **conducta
  visible**, no por símbolo. Sin población (bloqueo 5) no hay con quién hablar.

### 4.3 Cómo se operacionalizaría con reglas locales (desde mundo y medida)

- **Nodo** = código exacto (ya existe, `ncod`) + su **vector de consecuencia** `ΔS` observado (ya existe: `EFECTO` lo da al
  cuerpo; falta guardarlo por token, EMA local de `ΔS` por código: 2 números por nodo).
- **Arista "es una variable de lo mismo"** = **misma consecuencia para el cuerpo**, no mismos píxeles. Regla local: al morder un
  token nuevo cuyo `ΔS` coincide en signo con el de un token conocido y cuyos códigos comparten ≥ 2 celdas, la arista se
  escribe (un escalar de confianza) y el valor **se presta** por la arista con la fracción de confianza; una mordida con
  `ΔS` de signo contrario o `R = 0` la **corta** (B-5 ya hace el corte por división; el préstamo es el mecanismo de B-4, que
  desliga en 1 mordida 3/3). Nada de esto exige gradiente.
- **Mundo que lo mide** (bloqueo 3): familias con `ΔS` compartido y excepciones raras; **medida**: exposiciones hasta asociar
  la variante (predicción honesta: 1–3 contra 16) y herencia falsa en la excepción (debe caer a 0 en ≤ 2 mordidas por el
  corte); **control decisivo**: familia barajada (variantes con `ΔS` al azar) — la arista no debe ayudar; `px0`/`azar` de la
  batería de generalización intactos.
- **"Lenguaje"** sólo después y sólo en población: el token que un cuerpo emite (la conducta + / − de N1, honesta) y que otro
  liga a su propio nodo por co-ocurrencia; la medida es la de N1 (mordidas hasta criterio del novato) y el control es la
  señal barajada (ya validado como destructivo).

**Evaluación honesta.** La hipótesis describe con precisión lo que el organismo hace a medias (tokeniza y vectoriza; presta
valor por parecido; corta cuando el mundo desmiente) y nombra lo que le falta (aristas explícitas y un otro). Pero desde
esta lente el cuello no está en la representación sino en **el mundo y la medida**: sin familias de estímulos, sin muerte
real y sin población, "sal rosa es sal" no se puede medir y "lenguaje" no tiene interlocutor. El grafo entra por el mismo
método que todo lo demás (ancla, preregistro, réplica), y su primera prueba no es XOR sino **exposiciones hasta asociar una
variante en un mundo con familias** — la medida que el director fijó a las 05:10.

---

## 5. Resumen de orden sugerido (no decisión; la decide el director)

1. Mundo de población con muerte real y herencia (bloqueos 1, 2, 5), con su ancla y su medida de validez. Antes de él,
   correr el bloque 2 de reproducción tal como está preregistrado (261–280) para cerrar la línea "reproducción como conteo"
   con su propio criterio, sin declarar reproducción.
2. Mundo con familias y renovación simétrica (bloqueo 3): es donde se mide la hipótesis del director.
3. Coste de la mordida inútil o boca que lee `ΔS` (bloqueo 4): barato, y devuelve la conducta como medida.
4. B-5 al tronco (candidato a v15): la única pieza declarada hoy que hace falta para que "variable de lo mismo" no se convierta
   en "lo mismo".
