# DIAG sala 2 — lente REPRESENTACIÓN Y CÓDIGO (18 sep 2026, ~09:45)

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales (sin backprop en el
runtime) que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada. Primero llegar a la
frontera; segundo, que viva.

**Lo que hice y lo que no.** Leí `CLAUDE.md` (día 7), `PLAN.md`, `HANDOFF.md` §13 y §15.7–15.8, el registro del 18 sep desde
ERR-35 hasta ERR-42, `ENJAMBRE_xor_20260918.md`, `PUENTE_creacion.md` (A12–A16, B1–B6, B-4, B-5), los tres preregistros
(v15e, mundo vivo, reproducción) y `organismo/organismo_v14.py` entero. **No edité ningún archivo del repo**; este es el único
archivo nuevo. **No corrí el organismo ni ningún `Pool`.** Hice un solo cálculo estructural de muestreo (3 000 matrices `KW`
sorteadas como en `run()`, `code(P)` = top-3 de `KW@P`; script en mi scratchpad, 4 s, sin simular un paso) para tener
números propios de la lente; los doy como lo que son: geometría del código, no resultados de organismo.

---

## 0. Resumen en diez líneas

1. El tronco v14.1 representa con **dos vectores y ningún nodo**: la retina `P ∈ {0,1}⁶` y el código de Kenyon
   `k ∈ {0,1}⁹⁰` con 3 unos (K = 3). Todo lo que "sabe" es valencia: `Wp − Wn` por celda y `Wps − Wns` por píxel.
2. Lo más parecido a un **token** es `_key(kc) = frozenset` de 3 índices (`ncod`, línea de la puerta por código). Sirve
   sólo para contar mordidas; no tiene valor propio, no tiene aristas, no nace al ver: nace al morder.
3. **"Sal rosa" cuelga de "sal" por accidente, no por decisión**: con 2 de 3 píxeles iguales el código nuevo comparte
   0/1/2/3 celdas con probabilidad 0.17 / 0.49 / 0.31 / 0.03 (media 1.21 de 3 → hereda ~40 % del valor rápido, y por semilla
   entre 0 % y 100 %). Con un píxel añadido: 0.03 / 0.29 / 0.53 / 0.14 (media 1.78 → ~59 %). Dos estímulos sin ningún píxel
   común comparten una celda el 26 % de las veces. La vía lenta sí hereda por regla (lineal en 6 px): es la única
   "variable de lo mismo" que el tronco tiene, y sólo para relaciones lineales.
4. El código es un **hash que colisiona por diseño**: 6.8 % de semillas con colisión entre A–D (crudo), 86 % con los 20
   patrones de peso 3 (registro: 18/200 y 170/200). El único órgano que separa códigos es la fisión por **conflicto de
   signo** (`Wb[c]·R < 0`); con `R = 0` no actúa (alias de la sal: |W[sal]| 1.45, veneno −1.45, evitación ×7). B-5 lo repara
   (18/18 semillas) y **no está en el tronco** (decisión del director).
5. La **memoria de pares** (M3) cruza XOR con 8 ejemplos (1.000, n\* = 7–10) y ningún candidato entra: v15d no se desdice
   (E2 0/20) y deja a la rápida sin consolidar (E1 0/20); v15e arregla E1/E2 (humo −2.97 / +1.00) y pierde XOR (0.250
   contra 0.375 en una semilla, gana (2,4)); v15f (R crudo + relevo) está propuesto, no construido.
6. **Nada nace por novedad.** Una celda sólo se recluta cuando dos recompensas de signo opuesto caen sobre la misma celda
   consolidada. Un estímulo nuevo lee 3 proyecciones aleatorias ya existentes; 46–55 de 90 celdas activas no llevan valor
   legible (B1).
7. **Sin morder no hay nada** (C-P5: "la única fuente de información del organismo son sus propias mordidas"). Como la
   identidad y el valor son la misma memoria, un estímulo con `R = 0` no deja traza (sal muda: 0 divisiones, 0 valor).
8. El mundo vivo muestra el camino por el que sí se "plantea como variable de lo mismo": **un índice más en la memoria**
   (fila por necesidad) resuelve el XOR necesidad × estímulo (1.0 contra 0.5 escalar, 20/20 ×2, 11 exposiciones). No es
   un lector mejor: es una memoria indexada.
9. B-4 midió la condición necesaria del grafo del director: aristas de parecido legibles exigen un código graduado
   (HD nh = 2000, kh = 40: 0.025 / 0.075 / 0.225 para 0/1/2 px comunes); el Kenyon del tronco da 0.000 / 0.000 / 0.333 y
   **no ordena vecinos**; y en el mundo del tronco el parecido **contradice** el valor (el único par parecido es
   comida/veneno). Su prueba decisiva (mundo de regla `px0` contra `azar`) **no se ha corrido**.
10. "Eso es lenguaje" no se puede declarar con nada de lo medido (regla 6 y 8): N2 cerrado con dos mundos; lo que transfiere
    es la conducta visible (N1 7–8 mordidas contra 19; N3d 0.81). Lo declarable hoy: *asocia, revierte, generaliza lineal,
    XOR con prior de pares, valor por necesidad, alias de código y su reparación fuera del tronco*.

---

## 1. Qué es hoy la representación del tronco (v14.1, `organismo/organismo_v14.py` feefc88b1fd8d434), leída línea a línea

| pieza | qué es exactamente (línea) | memoria | qué decide |
|---|---|---|---|
| retina | `PAT`: 4 patrones binarios de peso 3 sobre 6 px (A, B, C, D), de los C(6,3) = 20 posibles | 0 | el mundo |
| proyección | `KW ∈ ℝ^{90×6}`, 30 filas activas al nacer, `U(0,1)`; `cond()` rechaza `KW` hasta que `code(A) ∩ code(B) = 0` | 540 | azar + `cond()` |
| código | `code(P) = argsort(KW@P)[-3:]` → `kenyon(P)`: indicador de 3 celdas de 90 (K = 3) | 0 | `KW` |
| valor rápido | `Wp, Wn ∈ [0,3]⁹⁰`; `W = (Wp−Wn)@k`; regla delta con **su** error `dlt = R − _wf`; drenaje `lam·min(Wp,Wn)` | 180 | morder |
| valor lento | `Wps, Wns ∈ [0,10]⁶`; lectura lineal `(Wps−Wns)@P`; `eta_s = 0.15`, **su** error `R − _ws` | 12 | morder |
| puerta | `_fam(k)`: familiar si `ncod[key] ≥ 5` y ≥ 1 celda del código con `|Wb| > 0.2` → rápida; si no → lenta | `ncod` (dict) | ruteo en la boca |
| token | `_key(kc) = frozenset(np.flatnonzero(kc))`; `ncod[_ky] += 1` sólo dentro de `if mordio:` | 1 entero por código mordido | sólo la puerta |
| estructura | fisión (`div_signo`): si `Wb[c]·R < 0`, `|Wb[c]| > 0.2`, `kj@P > KW[c]@P` y hay celda libre → hija `KW[j] = clip(0.95·KW[c] + 0.5·dist, 0, 5)·_rel` (ciega fuera de `P` y a lo irrelevante, `mask_rel = 2`), madre fija, valor fisionado por signo | hasta 90 celdas | conflicto de signo |
| lo que NO hay | nodo por estímulo · arista entre estímulos · prototipo guardado · valor por contexto · escritura sin morder · reclutamiento por novedad | — | — |

**Qué es un "token" aquí, con precisión.** El único objeto discreto con identidad es `_key(kc)`: existe desde la primera
mordida de ese código exacto, cuenta mordidas, y la boca lo consulta sólo para elegir vía. El valor no está en el token:
está repartido en 3 celdas que ese token **comparte** con cualquier otro patrón que caiga en ellas. Por eso el registro
puede decir "la generalización de v9 era su interferencia" (fuga 1 de 3 celdas) y por eso el alias existe: dos tokens
con el mismo `frozenset` son **indistinguibles** para la vía rápida, para la puerta y para la fisión (que exige `R ≠ 0`).

**Geometría del código, medida hoy (3 000 `KW`, sin `cond()`, sin correr el organismo):**

| relación entre dos patrones | \|code ∩ code\| = 0 | 1 | 2 | 3 (mismo código) | media (de 3) |
|---|---|---|---|---|---|
| 0 px comunes | 0.716 | 0.263 | 0.021 | 0.000 | 0.31 |
| 1 px común | 0.467 | 0.440 | 0.090 | 0.003 | 0.63 |
| **2 px comunes ("sal" → "sal rosa" por canje de un píxel)** | 0.165 | 0.492 | 0.312 | **0.031** | **1.21** |
| **superconjunto ("sal" → "sal + 1 px")** | 0.034 | 0.294 | 0.529 | **0.143** | **1.78** |

Semillas con algún par idéntico entre los 20 patrones de peso 3: **0.864** (registro, `negativo_codigo.py`: 170/200);
colisión entre A, B, C, D sin `cond()`: 0.068 (registro con `cond()`: 18/200 = 9 %). Lectura: la vía rápida trata a "sal
rosa" como "sal" en una proporción **aleatoria por semilla** (0 %, 33 %, 67 % o 100 % del valor), y en 1 de cada 7
semillas un píxel añadido produce **el mismo código** (alias total). Un grafo convertiría esa proporción en una
decisión (arista o no) en vez de un accidente de `KW`.

---

## 2. Dónde está exactamente la frontera hoy (números, con fuente)

**Tronco v14.1** (`feefc88b1fd8d434`; examen v3′ 8/8 en 121–140, 141–160 y 161–180, 7/8 en 101–120 por la semilla 117;
`bateria_generaliza` G1 1.000 / G2 0.94–0.97 ×3; capacidad N\* 51 de 60; 3T-k 0.237 con 53 celdas; `REGISTRO` 05:05 y
06:05). Retiene 20/20 y generaliza **lineal** (px0) a 1.000; compone historias de hasta 3 pasos; recupera de la inversión.

**Nivel 3 no lineal (XOR), cerrado por ERR-35 (07:47):** con 8 ejemplos 9 de 15 hipótesis empatan (gradiente exacto 0.562,
backprop 0.531, fisión 0/20); **con 14 ejemplos** la regla local llega a 1.000 (n\* = 200); **con 8 y prior de pares** (M3:
15 celdas × 4 casillas, escritura de un golpe, argmin de error propio) 1.000 / 1.000 en dos series, n\* = 7 y 10
(`xor_7_s121-140`, `xor_7_s141-160`). **Ninguna versión entra al tronco:** v15c V1 sin medir (ERR-38 anuló su G1; corregido
1.000); v15d G1 1.000 / G2 0.999, xor01 0.875 estricta, **pero E2 0/20 y E1 0/20** (la tabla no se desdice y la rápida no
recibe mordidas: lee 1.45·R = −4.35); v15e (`PREREGISTRO_v15e.md` §8, humo de un proceso): E1 −2.97 / −2.99, E2 +1.00 /
+1.00 **arreglados**, y xor01 s141 **0.250 < 0.375 OFF** con ganadora (2,4): "una tabla que guarda lo que a la lineal le
falta hereda el fracaso de la lineal". Serie no corrida; v15f (R crudo + relevo) propuesto (A16), no construido.

**Nivel 4, alias de código (08:10–09:12):** 2/20 semillas del mundo vivo (182, 188) con `|code(sal) ∩ code(veneno)| = 3`;
bloque de la sal (9 ALIAS / 9 LIMPIAS): |W[sal]| 1.45 contra 0.0, veneno −1.45 contra −3.0, exposiciones 3 835 contra 545,
0 divisiones; persiste sin sed (1.62) y la puerta de v13 no lo repara (1.48). **B-5** ("cuando una celda con valor recibe
nada bajo una retina distinta, divide"): 18/18 ALIAS → |W[sal]| 0.0, veneno −3.0, exposiciones 517/475, muertes 41 contra
75/77, celdas 37; **tronco idéntico** (examen 8/8, generalización 40/40, inercia por construcción). DECLARADO; candidato a
v15; **no está en el tronco**. Negativo estructural: en el mundo de regla 135/200 semillas tienen un patrón de test que lee
exactamente la celda de uno de entrenamiento (291 fugas, 115 de valencia opuesta) → parte de G1 es alias.

**Grafo (B-4, mini-prueba de 3 semillas, `organismo_v14L.py`):** v14 necesita **16** mordidas para asociar un patrón nuevo
débilmente parecido (C veneno) y 8 para el engañoso (D comida con 2 px de veneno). Ligar y heredar por la vía lenta baja a
13 (3/3) en el débil y **sube a 11–13 en el engañoso** (3/3), contaminando `W_B` de −2.97 a −4.2/−5.5 (el préstamo cae en
celdas compartidas); desligar cuesta **1 mordida** (3/3). Diagnóstico: el Kenyon no ordena vecinos (0.000 / 0.000 / 0.333),
el HD sí (0.025 / 0.075 / 0.225); en el mundo del tronco el parecido contradice el valor. **Prueba decisiva no corrida:**
`exp_hasta` en el mundo de regla con `px0` (el parecido predice) contra `azar` (no predice).

**Mundo vivo (181–200 y 201–220):** valor por necesidad → xor01 necesidad × estímulo 1.0 (20/20 ×2), ESCALAR 0.5,
BARAJA_CON 0.5, tabla 2 × 4 exacta en ~11 exposiciones; muere 28–41 % menos. Peldaño 2: la medida `descendientes_viables`
se tiró (P-R1: ESCALAR 36 y BARAJA_CON 39.5 "descendientes" muriendo 1.5×); saciado, `min(E, Ag)` veta la sal (0.797 → 0.007)
y CUELLO_MIN (65.5) ≥ tercera fila (55): la tercera necesidad sobra.

**Aprender sin morder:** C-P5 refutado; N2 cerrado con dos mundos; C-P6 nulo (SOLO_R 0.986 fuera de banda) y su réplica
tampoco (N1 13/20). La frontera, en una frase: **el organismo aprende, revierte, generaliza lo lineal y XOR con prior, y
sobrevive con dos necesidades; no tiene ningún objeto que sea "un estímulo" aparte de su valor, ningún vínculo entre dos
estímulos que no sea compartir celdas al azar, y nada de lo que descubrió esta mañana (pares, desambiguar, filas) está en
el tronco.**

---

## 3. Bloqueos, ordenados por importancia (desde esta lente)

### B1 — No existe el nodo: la identidad de un estímulo es "las celdas que comparte"

- **Evidencia.** `organismo_v14.py`: el valor vive en `Wp/Wn` por celda; `_key(kc)` sólo cuenta mordidas. Geometría medida hoy:
  0 px comunes → 26 % comparten una celda; 2 px comunes → hereda 0/33/67/100 % del valor con p = 0.17/0.49/0.31/0.03. B1
  (PUENTE): 46–55 de 90 celdas activas sin valor legible. B-4: el Kenyon da similitud 0.000 / 0.000 / 0.333 (no ordena
  vecinos). "La generalización de v9 era su interferencia" (`CLAUDE.md`, fuga 1 de 3 celdas).
- **Por qué bloquea.** "Sal rosa cuelga de sal" exige (a) un nodo para "sal" y (b) una arista. Hoy no hay ni (a) ni (b): la
  relación entre dos estímulos es un accidente de `KW`, no una decisión del organismo, y por eso no puede aprenderse ni
  desaprenderse (una arista se corta; una celda compartida no). También bloquea "aprender sin morder": sin nodo no hay
  dónde escribir un encuentro que no muerde.
- **Qué lo desbloquearía.** Un nodo por código exacto **que nazca al VER** (llegada al objeto, `pos in objs`), con prototipo
  `P` (6 floats), slot de valor propio y contador; el valor sigue escribiéndose sólo al morder. Separa "qué" de "cuánto vale".
  Es la pieza mínima del grafo del director. Detalle en §4.6.
- **Coste.** ≤ 9 números por nodo (≤ 20 nodos en los mundos actuales); búsqueda determinista sin rng (identidad apagada bit
  a bit); una tercera puerta en la boca (nodo propio → herencia por arista → lenta). Un humo de un proceso, dos bloques
  `Pool` (~10 min), examen + generalización (~8 min). Riesgo: en el mundo del tronco (2 estímulos, A·B = 1 px) nunca nace
  una arista → el examen no lo mide; lo mide el mundo de regla y el mundo vivo (como con B-5).

### B2 — El código colisiona por diseño (K = 3 de 90 sobre 6 px) y sólo el conflicto con signo separa

- **Evidencia.** Colisión 9 % con 4 estímulos (18/200), 85–86 % con 20 patrones (170/200; mi muestreo 0.864); alias de la
  sal (1.45 / −1.45 / ×7 / 0 divisiones; S-5 persiste sin sed; S-6 la puerta no repara); fuga px0 135/200 semillas en el mundo
  de regla. B-5 repara 18/18 y es inerte en el tronco (40/40 idénticos) → **no está en el tronco**.
- **Por qué bloquea.** Cualquier mundo con más de 2 estímulos —el mundo vivo, el de regla, cualquier "sal rosa"— hereda el
  alias: el que no informa roba el valor y el que informa pierde la mitad del miedo, y la evitación impide corregir. Un grafo
  sobre este código heredaría las colisiones como aristas falsas de peso 1.
- **Qué lo desbloquearía.** (i) Entrar B-5 al tronco como v15 (perilla `desambiguar`; coste 0 medido). (ii) Reportar
  siempre la geometría del código del mundo (`negativo_codigo.py`, 0.1 s) junto a cada bloque. (iii) Para el nodo de B1,
  indexarlo por `(código, P)`: dos estímulos con el mismo código y retina distinta son dos nodos aunque compartan celdas.
- **Coste.** (i) decisión del director + gemelo numba de B-5; (ii) cero; (iii) 6 floats por nodo.

### B3 — La única vía que generaliza es lineal en 6 px; la memoria de pares no entra porque no se desdice o pierde XOR

- **Evidencia.** G1 1.000 (px0) con `Wps − Wns`; XOR 0.50 con rasgos propios; M3 1.000 con prior (n\* 7–10); v15d E2 0/20 y E1
  0/20; v15e humo: E1/E2 arreglados, xor01 0.250 (ganadora (2,4)); v15f no construido. ERR-41: los V2b de v15c/d corrieron en
  configuración tipo v13.
- **Por qué bloquea.** "Variable de lo mismo" con relación no lineal ("sal rosa vale distinto que sal en cierto contexto")
  no tiene sustrato: la lenta sólo puede representar `valor(sal) + w[rosa]`. Y la única pieza que representa conjunciones
  (la tabla de pares) todavía no coexiste con revertir.
- **Qué lo desbloquearía.** v15f: casilla con **R crudo** + sobrescritura + relevo hacia la lineal en casillas no vistas, cada
  vía con su error (predicción de A: E1/E2 como v15e, xor01 0.80–0.88). Y, desde esta lente, poner la tabla **en el nodo**
  (B1) y no en la vía lenta: la casilla del nodo es la "variable de lo mismo" con contexto.
- **Coste.** Un preregistro + constructor por anclas (dos anclas respecto de v15e) + humo (1 proceso) + serie 101–120 /
  141–160 (~15 min `Pool`). Riesgo declarado: px0 < OFF si la ganadora no contiene el píxel 0 en ≥ 3/20.

### B4 — La memoria sólo guarda valencia: no hay "qué" sin "cuánto vale", y sin morder no hay nada

- **Evidencia.** Todo el estado aprendible es `Wp, Wn, Wps, Wns, KW, mu` — ninguno se escribe fuera de `if mordio:` (salvo
  `Wl`, la política). Sal muda: 0 divisiones, 0 valor (S-4). C-P5 refutado (la codificación predictiva no baja exposiciones).
  A-6/A12: con 8 patrones "nadie puede", pero además **antes de la sonda los otros 12 patrones no existen en el mundo**
  (`tipos.extend(test)` en `fase2_en`). Mundo vivo: lo que compra el XOR natural es **un índice más** (fila por necesidad),
  no un lector mejor (ESCALAR 0.5 contra 1.0).
- **Por qué bloquea.** La medida que manda desde el 05:10 es *exposiciones hasta asociar*; con esta memoria la cota es el
  número de mordidas (v14: 16 para un patrón nuevo). Un organismo que no guarda "lo vi junto a X" ni "lo vi sin sed" no
  puede asociar en una exposición: no tiene dónde. Y N2/N3 (significado) mueren por lo mismo: el único contenido
  transferible es la valencia.
- **Qué lo desbloquearía.** Escritura local **al encuentro** (no al morder) de relaciones sin valor: co-ocurrencia con el
  nodo anterior, necesidad activa, sitio. El valor sigue llegando por la mordida (regla delta, que revierte). El mundo vivo
  ya demostró la mitad: la fila por necesidad es exactamente "el mismo nodo, otra variable".
- **Coste.** Memoria por arista (2–3 números) y un `Generator` aparte si hace falta azar; mundos donde las relaciones
  predigan el valor (regla `px0`; mundo vivo con 4–5 estímulos). Cuidado con la trampa 3: lo rechazado se queda en el
  anillo (veneno ×6.3 más encuentros que comida): la co-ocurrencia estará sesgada por el muestreo y hay que reportarla
  por exposición.

### B5 — La estructura sólo nace por conflicto, nunca por novedad

- **Evidencia.** Fisión: `Wb[c]·R < 0 and |Wb[c]| > 0.2 and kj@P > KW[c]@P`. Un patrón nuevo lee 3 proyecciones existentes;
  la hija sólo nace cuando dos recompensas contradictorias caen sobre una celda consolidada. B1 (PUENTE): duplicar el pool
  a 180 no devuelve nada; lo que se agota es la evidencia por código; capacidad N\* 51 de 60 con la puerta. 3K (día 3):
  aprender `KW` no mejora la generalización.
- **Por qué bloquea.** "Que un símbolo nazca" hoy sólo ocurre como reparación posterior a un daño (y con `R = 0`, ni eso sin
  B-5). Un nodo que nace al ver (B1) es la versión proactiva; ART lo llama compromiso por vigilancia (ya citado en
  `LITERATURA_novedad`: "ya existe"). No hace falta reclutar celdas de `KW` (rompería el rng y el ancla): basta el nodo.
- **Qué lo desbloquearía.** Lo mismo que B1: nacimiento por novedad de código exacto o de prototipo (`|P − P_j|₁ > 0` con el
  mismo código = alias), sin tocar `KW`.
- **Coste.** El de B1. Inerte en el mundo del tronco salvo el conteo (2 códigos), así que el examen v3′ debe salir idéntico:
  se verifica por identidad, no por criterio.

### B6 — (instrumento) La geometría del código no está en ninguna batería

- **Evidencia.** `negativo_codigo.py` (0.1 s) existe desde las 08:55 y no lo corre ningún runner; ERR-37 tardó dos series en
  atribuir la "superstición" al alias; ERR-38 mostró que 6/40 filas idénticas al 16.º decimal eran la vía lenta apagada.
- **Por qué bloquea.** Sin la tasa de colisión y la similitud código–retina reportadas por mundo, cada resultado de
  generalización mezcla regla y alias (135/200 fugas en px0) y cada "superstición" es un ERR futuro.
- **Qué lo desbloquearía.** Una línea en cada runner: nº de pares con el mismo código, nº con 2/3, fugas test→train, y
  celdas con valor legible al final. Coste: cero CPU, media hora de un implementador.

---

## 4. La hipótesis del director, desde esta lente

> "Si sal es sal será número uno, lo guardo, lo vectoriza; y después sal rosa lo vectoriza, marca como sal y lo plantea
> como una variable de lo mismo — eso es lenguaje. Ahora, si pensamos en el aprendizaje, y ya lo hemos visto, que puede
> aprender y desaprender." (09:40) · "La palabra es grafo, no vectorización." (05:10)

### 4.1 Traducción frase a frase a lo que el tronco tiene

| frase del director | pieza del tronco | ¿lo hace? | número |
|---|---|---|---|
| "sal es sal, será número uno" (token) | `_key(kc)` = frozenset de 3 celdas, en `ncod` | **a medias**: nace al morder, cuenta mordidas, no tiene valor ni aristas | 1 entero por código |
| "lo guardo" | `Wp/Wn` en las 3 celdas; `Wps/Wns` en los 3 px | **sí**, pero guarda valencia, no identidad | W −3.0 exacto (E1) |
| "lo vectoriza" | `P ∈ {0,1}⁶` → `KW@P` → `k ∈ {0,1}⁹⁰` | **sí**, dos veces (retina y Kenyon) | K = 3 de 90 |
| "sal rosa lo vectoriza" | el mismo camino | **sí** | — |
| "marca como sal" | vía rápida: celdas compartidas; vía lenta: píxeles compartidos | **rápida: al azar** (hereda 0–100 %, media 40 % por canje, 59 % por píxel añadido); **lenta: por regla**, sólo lineal | tabla §1 |
| "variable de lo mismo" | fila por necesidad del mundo vivo (mismo código, otra fila) | **sí, para la variable interna** (necesidad); **no** para un modificador del estímulo ("rosa") | xor01 1.0 contra 0.5 |
| "eso es lenguaje" | N1 (conducta visible), N2 (símbolo), N3d | **no declarable**: N2 cerrado ×2, C-P6 nulo; transfiere sólo la conducta | N1 7–8 contra 19 |
| "puede aprender y desaprender" | regla delta (rápida y lenta), fisión | **sí** (E1 20/20, E2 20/20); **la tabla de un golpe no** (v15d E2 0/20); **reescribible sí** (v15e humo, 1 mordida) | — |
| "grafo, no vectorización" | nada; B-4 (`v14L`) fuera del tronco | **no hay grafo**; B-4 midió la condición necesaria (código graduado) y el mundo del tronco la contradice | sim 0/0/0.33 contra 0.025/0.075/0.225 |

### 4.2 Lo que ya hace (medido)

- Tokeniza en el sentido débil: cada código exacto tiene una clave discreta y un contador (`ncod`), y la boca la usa.
- Vectoriza: retina y Kenyon. El valor rápido es un vector de 90; el lento, de 6; A-3 demostró que los dos canales son
  un vector con signo (identidad 60/60).
- Hereda por parecido, en dos regímenes: **por regla** (lenta, lineal: G1 1.000 en px0) y **por accidente** (rápida: la
  fuga de celdas; 26 % incluso sin ningún píxel común).
- Plantea "lo mismo" como variable de un contexto **interno**: fila por necesidad (1.0 contra 0.5; barajar el contenido
  lo destruye).
- Aprende y desaprende con la regla delta (revierte en E2, extingue en E2L); repara alias por fisión con B-5 (fuera del tronco).

### 4.3 Lo que no hace (medido o por construcción)

- No tiene un objeto "sal" independiente de "cuánto vale sal": sin mordida no hay nada (S-4, C-P5).
- No liga "sal rosa" a "sal" por decisión: lo hace `KW` con probabilidad; y cuando lo hace del todo (mismo código, 3 % por
  canje, 14 % por píxel añadido) es alias, que hoy es un defecto (la sal roba al veneno).
- No corta la herencia cuando el modificador cambia el valor: las celdas compartidas siguen compartidas (v9/v11: tapar la
  fuga costó la generalización; v13 la recuperó en la lenta).
- No representa conjunciones en el tronco (XOR sólo con prior en instrumentos aparte).
- No transmite ningún token: lo único que el otro organismo lee es la conducta (N1, N3d).

### 4.4 Grafo o vector (la corrección de las 05:10), con el dato

El tronco es vector puro. B-4 midió lo que un grafo necesita y no tiene: (1) un código cuya similitud **ordene** vecinos —
el Kenyon K = 3 da 0.000 / 0.000 / 0.333 (mi tabla: 2 px comunes → 0/1/2/3 celdas con 0.17/0.49/0.31/0.03; un vecino a 2 px
y uno a 0 px pueden compartir las mismas celdas); el HD (nh 2000, kh 40) da 0.025 / 0.075 / 0.225, graduado; (2) un mundo
donde el parecido **prediga** el valor — en el del tronco lo contradice (el único par parecido es comida/veneno) y heredar
cuesta (8 → 11–13). De ahí la lectura honesta: **el grafo no es una alternativa al vector, es una capa encima**: los nodos
necesitan un vector para tener aristas legibles (B-4: "la alta dimensión sí hace falta"), y el vector necesita nodos para
que la herencia sea una decisión revocable y no una fuga. La prueba que lo decide está escrita (B-4, mundo de regla `px0`
contra `azar`) y sin correr.

### 4.5 Aprender / desaprender, con precisión

Lo que revierte es la **regla delta** (cada vía con su error); lo que no revierte es **escribir de un golpe sin
sobrescribir** (v15d: E2 0/20) o con doble cuenta (1.45·R). v15e mostró en humo que sobrescritura + error propio devuelve
la reversión en una mordida **y** la consolidación de la rápida (49–58 mordidas de B, como v14.1), y que el precio fue
guardar residuos. La lección para cualquier nodo/arista: **escribir R crudo, sobrescribir, cada vía con su error**, y que
la lectura por nodo no quite mordidas a las celdas (la rápida aprende de mordidas, no de error: A16 §1).

### 4.6 Si fuera mi creación: cómo le daría vida (propuesta en el formato del puente; NO preregistro, NO construido, NO medido)

- **Hipótesis.** Separar *qué* de *cuánto vale* con un nodo por estímulo que nace al ver, y ligar cada nodo nuevo al más
  parecido por una arista revocable, baja las exposiciones hasta asociar un estímulo modificado ("sal rosa") de ≥ 10 a ≤ 3
  cuando el modificador no cambia el valor, y no daña (ni al padre ni al hijo) cuando lo cambia, porque la herencia vive
  en el nodo (no en celdas compartidas) y una mordida contraria corta la arista.
- **Mecanismo mínimo y memoria (cinco reglas locales; nada mira al futuro; sin gradiente):**
  1. **Nacimiento (al ver, no al morder):** en `pos in objs`, si `(key(kc), tuple(P))` no está en la tabla de nodos, se crea
     con prototipo `P`, valor propio `v = 0` (dos canales o vector con signo, A-3), `n_mord = 0`. Local: sólo ve `P` y su tabla.
     Indexar por `(código, P)` hace que dos estímulos con el mismo código y retina distinta sean dos nodos (alias resuelto
     **en la lectura**; en las celdas sigue haciendo falta B-5).
  2. **Arista "variante de":** al nacer, el nodo se liga al nodo existente con `|P ∧ P_j|` máximo si ≥ 2 (dos píxeles
     comunes o superconjunto); empate → sin arista (no rng) o `Generator` propio `seed+600000` (convención `v13s`). Guarda
     `padre`, `fiab ∈ [0,1]` (inicial 0.5). Memoria por nodo: 6 + 2 + 1 + 2 = 11 números.
  3. **Lectura en la boca (tercera puerta, simétrica a la de v13):** si el nodo tiene valor propio consolidado
     (`n_mord ≥ 1` y `|v| > 0.2`) → `v`; si no y tiene arista → `fiab · v_padre`; si no → lo que hoy hace v14.1 (rápida si
     familiar, si no la lenta). Así el préstamo **nunca toca `Wp/Wn`** (B-4 contaminó `W_B` a −4.2/−5.5 por prestar en celdas).
  4. **Escritura al morder:** `v ← v + eta_n·(R − v)` con **su propio** error (revierte); las celdas y la lenta siguen
     aprendiendo exactamente como en v14.1 con sus errores (la rápida necesita mordidas, no error: no se le quita ninguna
     porque la lectura del nodo sólo cambia `pb`, y `pb` con `fiab · v_padre` es la del padre, es decir la misma que v14.1
     tendría si ya lo conociera).
  5. **Desligar y fiabilidad:** si `R · (fiab · v_padre) < 0` en la primera mordida → arista cortada (`fiab = 0`, B-4: 1
     mordida, 3/3) y `fiab_tipo ← 0.7·fiab_tipo` (una EMA por tipo de arista: "2 px" / "superconjunto"); si confirma,
     `fiab_tipo ← 0.7·fiab_tipo + 0.3`. B-4 avisó: la señal es más rara que el problema en el mundo del tronco; por eso el
     mundo de prueba debe tener modificadores frecuentes (abajo).
  - **Qué NO hay:** cambio en `KW`, en la fisión, en la puerta de v13, en `Wl`; escritura de un golpe en celdas; planificador.
    Con `nodos = 0` es v14.1 bit a bit **sin consumir rng** (regla 2 de EQUIPO).
- **Instrumento.** `construye_nodos.py` → `organismo_v14N.py` por anclas desde `organismo/organismo_v14.py`
  (feefc88b1fd8d434, sólo lectura); `organismo_v14gN.py` desde `organismo_v14g` (mundo de regla, kwargs EXACTOS del tronco,
  regla 14 / ERR-41); `organismo_vivoN.py` desde `organismo_vivo.py` (20c0961c79de8825) con un **quinto estímulo "sal rosa"**
  = D con un píxel canjeado o añadido (el mundo del director), en dos variantes: *misma valencia* (informa como la sal) y
  *engañosa* (informa como el agua). Ancla: con 4 estímulos y `nodos = 0` ≡ `organismo_vivo`; con 2 estímulos ≡ v14.1.
  Arnés de identidad como `identidad_codigo.py` (42/42 de B-5 es el listón). Medida: `exp_hasta[nodo]` (B-4, sólo lectura).
- **Predicción numérica (para poder equivocarme).**
  - P1 mundo vivo, "sal rosa" de la misma valencia: `exp_hasta` ≤ **3** (v14.1/vivo: ≥ 8–16, el número de B-4) en ≥ 15/20;
    tabla 2 × 5 exacta en ≥ 18/20.
  - P2 "sal rosa" engañosa: desliga en **1** mordida en ≥ 18/20; `exp_hasta` ≤ vivo + 2; **`|ΔW[padre]| ≤ 0.1`** (B-4 dañó al
    padre 1.2–2.5): éste es el criterio que distingue "préstamo en el nodo" de "préstamo en celdas".
  - P3 mundo de regla (**el control decisivo, B-4 sin correr**): con `px0` (el parecido predice) `n*` ≤ 3 contra ≥ 10 OFF en
    ≥ 15/20; con `azar` (no predice) `n*` ON − OFF ∈ [−1, +1] y `fiab_tipo` termina ≤ 0.3. Si con `azar` también baja: fuga.
  - P4 tronco: examen v3′ 8/8 y G1 1.000 / G2 ≥ 0.94 con la perilla ON en 101–120 — esperado por **identidad** (A·B = 1 px:
    ninguna arista nace), como B-5 (T1/T2 idénticos).
  - P5 alias: en las 9 semillas ALIAS del bloque de la sal, el nodo de la sal lee **0.0** en ≥ 8/9 (las celdas siguen en
    −1.45: se reporta al lado) y con `desambiguar = 1` además el veneno vuelve a −3.0.
- **Control que puede fallar.** (a) `azar` (P3); (b) aristas barajadas (ligar al nodo equivocado: debe dañar como B-4
  engañoso); (c) herencia sin desligar (debe dañar); (d) identidad OFF; (e) la trampa 3: la sal rosa rechazada inunda el
  anillo → reportar exposiciones por estímulo, nunca agregadas; (f) la trampa nueva del mundo vivo: con déficit alto la
  boca muerde cualquier cosa (`W = 0 → pb 0.84`) — `exp_hasta` se lee por valor, no por conducta.
- **Mini-prueba (un proceso, 3 semillas, T = 100 000) antes de gastar un preregistro:** mundo vivo + "sal rosa" misma
  valencia y engañosa, ON/OFF pareado; mundo de regla s141 `px0`/`azar` ON/OFF. Se espera: `exp_hasta` 2–3 contra 8–16;
  desligue 3/3; `|ΔW[padre]|` ≤ 0.1; `px0` baja, `azar` no. Si `azar` baja: no se preregistra.
- **Coste total.** Constructor + arnés (2–3 h de un implementador); humo 1 proceso (< 1 min); dos bloques `Pool` (~10 min
  cada uno) + examen/generalización (~8 min); gemelo numba después. Memoria: ≤ 11 × nº nodos (≤ 25 en los mundos de hoy).
- **Lo que me tumba (y qué diría).** Si P1 no baja: la boca sigue leyendo la lenta porque el nodo nunca consolida (`|v| > 0.2`
  exige una mordida) → el órgano correcto es el préstamo, no el nodo, y se declara "liga pero no acorta". Si P2 daña al padre:
  el préstamo se coló en celdas (fallo de construcción, se ve en el diff). Si P3 baja con `azar`: la arista es una fuga y el
  grafo sobre 6 px no discrimina — cada patrón de peso 3 tiene 9 vecinos a 2 px de 20: **es plausible** que la retina de 6 px
  sea demasiado chica para un grafo (B-4 lo insinúa); entonces el siguiente paso es D = 10 px (`organismo_capB` ya lo usa) y
  se dice antes de correr.
- **Vocabulario si pasa (y sólo entonces):** *"liga lo nuevo a lo más parecido, hereda su valor sin tocar las celdas del
  padre, asocia en ≤ 3 exposiciones donde el parecido predice el valor y desliga en una mordida donde no"*. **Prohibido:**
  "lenguaje", "entiende", "razona por analogía", "tokeniza como un modelo de lenguaje".

### 4.7 Orden que propongo al coordinador (tres bloques, uno por vez, ninguno adelanta a lo ya en cola sin decisión del director)

1. **Cero coste, hoy:** la geometría del código en cada runner (B6) y la decisión sobre B-5 → v15 (B2).
2. **B-4 decisivo** en el mundo de regla `px0`/`azar` con `organismo_v14L` tal como está (instrumento listo, identidad 8/8):
   contesta si el parecido predice el valor en algún mundo antes de construir nodos. ~10 min `Pool`.
3. **Nodos** (§4.6) sólo si el bloque 2 muestra el contraste; si no, lo declarable es lo de B-4: *"lo que falta no es la
   ligadura sino una relación que prediga el valor"*, y el grafo espera a un mundo (o una retina) donde exista.

---

## 5. Lo que NO digo

No digo que el organismo tokenice, tenga símbolos, ni lenguaje. No digo que un grafo resuelva XOR (la tabla de pares ya lo
hace con prior; el grafo ataca *exposiciones hasta asociar* y el alias, no la conjunción). No digo que el nodo sustituya a
B-5: repara la lectura, no las celdas. Ninguna cifra de §4.6 está medida; las de §1 son geometría de `KW` (3 000 sorteos, 4 s,
sin simular), no resultados de organismo; todo lo demás está citado con su archivo y su entrada.

## 6. Archivos citados

`organismo/organismo_v14.py` (feefc88b1fd8d434) · `registro/REGISTRO_etapas_1_2.md` (ERR-35 → ERR-42; entradas 07:43,
07:47, 07:58, 08:06, 08:10, 08:16, 08:20, 08:38, 08:44, 09:07, 09:12, 09:16) · `registro/HANDOFF.md` §13, §15.7–15.8 ·
`registro/PLAN.md` (05:10 C: grafo) · `registro/investigacion/ENJAMBRE_xor_20260918.md` · `registro/investigacion/PUENTE_creacion.md`
(A12–A16; B1–B5; B-4 `organismo_v14L`; B-5) · `experimentos/creacion_A/PREREGISTRO_v15e.md` §1, §8 ·
`experimentos/creacion_B/PREREGISTRO_codigo.md` §3 · `experimentos/creacion_B/negativo_codigo.py` ·
`experimentos/nivel11_mundo_vivo/PREREGISTRO_mundo_vivo.md` §2, §9, §10 · `experimentos/nivel11_mundo_vivo/PREREGISTRO_reproduccion.md`
§3, §12 · `registro/investigacion/LITERATURA_novedad_20260918.md` §0 · `organismo/bateria_generaliza.py` (G1/G2) ·
script de muestreo: scratchpad de esta sesión (`geom_codigo.py`; no forma parte del repo).
