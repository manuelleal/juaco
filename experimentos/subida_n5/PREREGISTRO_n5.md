# PREREGISTRO: nivel 5, subida (equipo n5, 23-sep-2026): **V-5 = B-5 trasplantado a la tabla de referencia**

**MISIÓN (primero, siempre):** llegar a la AGI por este camino: un organismo mínimo con reglas locales, sin
retropropagación, que aprende, desaprende, generaliza, sobrevive y **se comunica con referencia**. Hoy: que el
mensaje refiera a la **FAMILIA Y a la VARIANTE con la misma tabla** (`BAR-T ≤ 5` **Y** `dist(PAR) ≥ 15`).

**Autor:** creador del equipo n5 (Opus). **Estado:** §0–§8 escritos **antes** del humo y de cualquier serie
(el arnés de identidad sí se corrió antes: regla 2). §9 (humo) se añade después y **no toca** §0–§8. Todo cambio
posterior va como candidato a ERR, con fecha, motivo y semillas nuevas. **Carpeta:** `experimentos/subida_n5/`
(no se toca nada fuera de ella; ningún congelado).

| | archivo | sha256(16) |
|---|---|---|
| constructor por anclas | `construye_v5.py` | ver `identidad_v5_salida.txt` (se imprime) |
| instrumento | `organismo_familias_v5.py` | `b6138d31e232b896` |
| runner (humo y serie) | `corre_v5.py` | `a543f997f6133764` |
| arnés de identidad | `identidad_v5.py` → `identidad_v5_salida.txt` | se imprime en la salida |
| **origen del instrumento (sólo lectura)** | `experimentos/nivel05_familia_variante_BAv/organismo_familias_bav.py` | `2dca0a3e239481f0` |
| **origen del runner (sólo lectura)** | `experimentos/nivel05_familia_variante_BAv/corre_familias_bav.py` | `4453754a9921e349` |
| ayudantes del arnés (sólo lectura) | `experimentos/nivel05_familia_variante_BAv/identidad_familias_bav.py` | `cf7655b379014a55` |
| tronco (sólo lectura) | `organismo/organismo_v14.py` | `feefc88b1fd8d434` |

---

## 0. Por qué este bloque y no otro (la elección honesta)

El nivel 5 está en 75 %. Lo que falta, según `ESTADO.md` (fila 5) y `HANDOFF.md` §13 (fila 5): (a) **familia Y
variante con la misma tabla** (hoy es "familia O variante"); (b) **N2**, significado emergente (línea cerrada
el 17-sep tras seis diseños; reabrirla exige cambiar el mundo **y** la recompensa); (c) **que el receptor
aprenda algo propio** (N3d mudo: obedece, no aprende; ERR-32 demostró que en ese montaje *no puede*); (d)
**XOR entre dos** (depende de N2). Elijo (a) porque es la única pieza con **causa medida** (la colisión de B,
37/37 semillas), **instrumento con identidad**, **criterio ya escrito y usado tres veces** (ERR-90) y un
mecanismo preregistrado **nunca corrido** (V-5 de C, 25 %). (b) y (d) mueven más puntos si funcionan, pero hoy
no tienen mundo decidible (teorema de C, REGISTRO 18-sep 06:30), y un bloque sin mundo no mueve nada.
**Lo que este bloque NO puede mover:** N2, lo propio del receptor, XOR entre dos. Su techo honesto son **+5 puntos**.

## 1. Lo medido de lo que parto (REGISTRO 5790–5833; verificado hoy sobre los crudos)

`BA-v` (dos tipos + min + conj_tipo = 2) pasa P1, P2, P4, P5 y R6 y **cae P6 en las tres series ERR-90**:
dist(PAR) 13/19, 14/18, 11/16. Releí los tres crudos (`serie_bav_*_crudo.json`): **en las 15 semillas que
fallan, `okP = 0` en las 15**: el receptor **muerde a la hermana** (T1v0, veneno) en su primera exposición tras
la entrega. `b6suf` (sufijo en todas las casillas) separa a la hermana (19/19, 18/18, 14/16) pero no al otro
token (BAR-T 8–12). `b5k3` hace lo contrario (dist 5–8; BAR-T 2–7).

**Causa, leída del código** (`organismo_familias_bav.py`, escrituras del mensaje y del bocado): el mensaje
`(T1v2, R = +1)` **y el primer bocado de T1v2** escriben +1 **por sobrescritura** en las 66 celdas, en la
dirección de T1v2. Esa dirección es la **misma** que la de la hermana en las 36 celdas de FORMA (misma familia) y
en una de las tres de VARIANTE (la colisión de B). La familia T1 es veneno: esas casillas decían −3. La
sobrescritura **borra la familia** y la hermana hereda el +1.

## 2. Hipótesis y mecanismo

> **H-V5.** Si una escritura que CONTRADICE a la casilla de la familia no la sobrescribe sino que la **parte**
> en una subcasilla de variante, el mensaje refiere a la variante (T1v2 se come) **sin** borrar la familia (la
> hermana sigue leyendo −3), y la misma tabla da familia **y** variante.

**Mecanismo mínimo (`v5 = 1`).** En cada escritura de la tabla (mensaje **y** experiencia propia), con `c` la
casilla de la familia (el bin de 2 bits de siempre) y `s` la subcasilla (bin, firma de los 3 px de variante
**de la retina presente**):
1. si `s` ya existe → la R va a `s` (la variante partida sigue aprendiendo de sus consecuencias);
2. si no, y `c` consta con `|valor| > 0.2` y **signo opuesto** a R → **se parte**: `s ← R`, `c` intacta;
3. si no → la escritura de siempre en `c`.
**Lectura:** `s` si existe; si no, `c`. Nada más cambia: ni el emisor, ni el canal, ni el mundo, ni la
elección de ganadoras, ni la boca, ni el rng del organismo (postcondición del constructor).

**Memoria nueva: NO es cero, y lo declaro.** Una tabla de subcasillas 66 × 32 (la forma del sufijo del bloque
6), poblada **sólo por conflicto**; `v5_sub` (subcasillas ocupadas) sale en cada corrida. Es menos que el
sufijo, que ocupa por defecto. **Desvíos respecto de B-5 del tronco, declarados:** no se guarda procedencia
("retina distinta" la pone la firma de la subcasilla); R = 0 no dispara (en este mundo no hay neutros); la firma
usa los px de variante que declara el mundo (el mismo supuesto estructural del bloque 6).

**Por qué hace falta partir también con el bocado propio, no sólo con el mensaje:** en el brazo CANAL la entrega
es por señalamiento (el receptor está ante T1v2), así que el primer bocado de T1v2 llega enseguida y también
sobrescribe. Si sólo partiera el mensaje, el bocado deshacería el arreglo.

## 3. Instrumento, anclas, identidad

`construye_v5.py` genera `organismo_familias_v5.py` (11 anclas sobre `organismo_familias_bav.py`, sha fijado;
aborta si cualquier ancla no aparece exactamente una vez; postcondiciones: mismo uso de `rng.`, ningún
Generator nuevo, `_esc5` ×3 y `_lee5` ×6, lectura de BA y baraja intactas) y `corre_v5.py` (runner de BA-v por
anclas: celdas nuevas, `v5` como perilla de celda en la regla 14, diagnóstico V-5 por corrida, contrastes).
**Arnés `identidad_v5.py`**: con `v5 = 0` ≡ `organismo_familias_bav` bit a bit (mundo AB, mundo del receptor con
las 5 lecturas, emisor, canal en 3 modos, brazo PAR, baraja, ancla larga de 120 000) y, por la cadena, ≡
`organismo_v14` (TRONCO) y ≡ `organismo_v15f_on`; inercia sin tabla; el prefijo hasta la entrega no cambia con
la baraja; mecanismo (partos por el mensaje, la hermana lee < 0 tras el mensaje, el referente > 0); perillas
mal escritas lanzan; tres controles que DEBEN diferir. **Resultado N/N en `identidad_v5_salida.txt`.**

**Regla 14:** el runner compara la entrada de cada celda × brazo campo a campo con la del bloque 6 y se para si
difiere en algo que no sea una perilla de celda (`v5` añadida a la lista). El humo lo imprime.

## 4. Brazos, celdas, emisor, semillas

- **Brazos:** los 7 del bloque 6, dirección (−) sola, sin tocar: `CANAL, CORTADO, BAR-H, BAR-T, VALOR, PAR, PAR0`.
- **Celdas (6):** `b4b` (base de R6, obligatoria) · `b6suf` y `BA-v` (**controles de instrumento**: deben
  reproducir sus series previas ±4) · **`BA-v5` (EL CANDIDATO)** · `BA-v5-sh` (**control que debe fallar**:
  memoria barajada) · `b5k3-v5` (**control de Occam que puede GANAR al candidato**: un tipo, k = 3, suma + V-5).
- **Emisor:** el del bloque 6 sin tocar (b4b bit a bit).
- **Semillas NUEVAS** (grep del 23-sep sobre `*.py *.md *.txt *.log` y nombres de archivo: ninguna aparece como
  semilla; `25711` aparece una vez como cuenta de mordidas en un log de la carrera): **serie 25701–25720,
  réplica 25721–25740, tercera sólo por §7 25741–25760; humo 25791** (banda 25781–25799; el runner rechaza
  cualquier otra). T = 100 000.
- **Puertas de montaje heredadas sin cambio:** P-I2 (emisor ≥ 18/20; P0 N ≥ 18), P-I4, P-I5 (se reportan).

## 5. PREDICCIONES NUMÉRICAS FIRMADAS (candidato `BA-v5`, en CADA una de las dos series)

| puerta (ERR-90, sin tocar) | predicción (rango) | prob. de pasar las dos series |
|---|---|---|
| P0 N ≥ 18 | 19 (17–20) | **70 %** (en 2101–2120 el emisor dio 16: riesgo del emisor, no del candidato) |
| P1 CANAL ≥ 15 | 17 (15–19) | 80 % |
| P2 CORTADO ≤ 5 | 0 (0–2) | 95 % |
| P3 BAR-T ≤ 5 | 4 (2–7) | 60 % |
| P4 VALOR ≤ 5 | 3 (1–5) | 75 % |
| P5 BAR-H ≤ 10 | **3 (0–6)** (BA-v: 7, 4, 9) | 85 % |
| **P6 dist(PAR) ≥ 15 y PAR0 ≤ 5** | **dist 17 (15–19)**, PAR0 1 (0–3) | **60 %: LA QUE PUEDE FALLAR** |
| P7 R6 muertes ≤ 1.5× b4b | **1.2× (0.8–2.0×)** | 55 % |
| P7 R6 okU ≥ okU(b4b) − 0.10 | 0.667 (0.583–0.833) | 60 % |
| MISIÓN (BAR-T ≤ 5 Y dist ≥ 15) | BAR-T 4, dist 17 | 45 % |
| **TODO (candidato)** | — | **20 %** |

**Contrastes pareados de la misma serie** (el runner los imprime como `K1`–`K4`, `I1`, `I2`):
- **K1:** `dist(BA-v5) − dist(BA-v) ≥ +3` → predigo **+4 (+2 a +7)**, 65 % en las dos.
- **K2:** `CANAL(BA-v5-sh) ≤ CORTADO(BA-v5-sh) + 3` → predigo CANAL 2 (0–4), 85 %.
- **K3:** `BAR-T(BA-v5) ≤ BAR-T(BA-v) + 2` → 80 %.
- **K4 (diagnóstico):** muertes BA-v5 / BA-v = 1.0× (0.7–1.5×). Predicción de mecanismo: V-5 **no** debería
  matar de hambre (la excepción T0v2, veneno en familia comida, ya no borra a su familia al morderse).
- **I1/I2 (instrumento):** b6suf dist ≥ 14 y BAR-T 8–12 (±4); BA-v dist 11–14 (±4). Si no, **no se lee nada**.
- **Occam `b5k3-v5`:** dist 16 (12–19), BAR-T 5 (2–8), BAR-H 4 (1–8); probabilidad de pasar TODO: 20 %.

## 6. Controles (incluido uno que puede ganar al candidato)

- **`BA-v5-sh` (memoria barajada):** misma R, casilla permutada. Si come igual que el candidato (K2 cae), el
  receptor come porque llegó un mensaje, no por lo que dice: **la línea muere** aunque pase todo lo demás.
- **`b5k3-v5` (Occam):** si pasa P0–P7 + MISIÓN igual que `BA-v5`, **la declaración es para la celda simple**
  ("V-5 basta con un tipo y la suma; los dos tipos sobran"). Puede ganar al candidato y lo digo antes.
- **`BA-v` en la misma serie:** la línea base exacta; K1 se mide contra ella, no contra las series viejas.
- **`b6suf`:** el sufijo en todas las casillas; si `BA-v5` no supera su BAR-T, V-5 no aporta sobre el sufijo.
- **`b4b`:** base de R6.

## 7. Criterio de veredicto y vocabulario (se aplica tal cual; nada se recalibra)

- **FUNCIONA:** en 25701–25720 **y** 25721–25740, `BA-v5` pasa P0–P7 y la MISIÓN, K2 pasa, I1 e I2 reproducen.
  *Permitido:* "con V-5 (la casilla de familia se parte cuando una escritura la contradice) la referencia es de
  familia **y** de variante con la misma tabla: BAR-T ≤ 5 y dist(PAR) ≥ 15 en dos series, el control barajado
  no lleva el mensaje y el coste no pasa de 1.5× la base". *Prohibido:* "lenguaje", "entiende", "comunica
  significado", "N2".
  **Si lo único que cae en UNA serie es P0 por el emisor** (N < 18) y todo lo demás pasa en las dos, se corre la
  **tercera 25741–25760** (regla 12) y se declara sólo si pasa entera.
- **HAY ALGO MODESTO:** K1 y K2 pasan en las dos series pero alguna puerta P1–P7 o la MISIÓN cae en alguna.
  *Permitido:* "V-5 repara la colisión de la hermana (dist +k sobre BA-v en la misma serie) pero no cruza la
  letra en …". *Prohibido:* "familia y variante con la misma tabla".
- **NO:** K1 cae en alguna serie, **o** K2 cae, **o** dist(PAR) < 15 en las dos. *Permitido:* "partir la casilla
  por contradicción no separa a la hermana" (o "la lectura no es referencial" si cae K2). Línea V-5 cerrada.
- **Instrumento roto:** I1 o I2 fuera de ±4 → no hay veredicto; se revisa el montaje (ERR-38).

**Puntos del nivel (propuesta; decide el director):** FUNCIONA → **75 % → 80 %** (se cierra "familia Y
variante"; quedan N2, lo propio del receptor y XOR entre dos). ALGO MODESTO → **75 %** (se registra la
reparación parcial; +0). NO → **75 %**, y la frase "familia O variante" queda como final de la línea.

## 8. Qué me refuta, y las cuatro trampas

**Refutaciones:** (1) K1 < +3 en una serie: partir por contradicción no llega a la hermana (quizá su primera
exposición llega por la vía rápida o la contaminación no es la de la tabla); (2) K2 cae: no hay referencia;
(3) P7 cae en las dos: "separa y vive peor"; (4) `v5_lee_par ≥ 0` en la mayoría de las semillas PAR: el
mecanismo no hace lo que digo aunque dist mejore por otra vía (se reporta, no rescata nada).

**Trampas (regla 5):**
1. *Canal simétrico:* no. El emisor es b4b bit a bit y no cambia entre celdas; el receptor recibe `(t, ref, P, R)`;
   CORTADO/PAR0 son gemelos mudos; BAR-H/BAR-T/VALOR prueban que importa el contenido; la baraja, la dirección.
2. *Acierto sin balancear:* no hay acierto: conducta binaria en la primera exposición, con puertas en los dos
   sentidos (P1 obliga a comer, P2–P5 a no comer; P6 exige comer una y no la otra en la misma vida).
3. *Mundo que se come la comida:* el mundo es el del bloque 4b/6 importado (renov = 1.0, deriva); V-5 no toca el
   mundo. El coste es puerta (P7) y se diagnostica (mordidas de comida/veneno, `frac_regalo`).
4. *Sitios fijos:* P-I4 exige que la primera exposición de la vida al referente sea la de la entrega; los
   patrones se regeneran por semilla. **Aviso honesto:** la firma de variante usa los px 9–11 que declara el
   mundo (supuesto estructural heredado del bloque 6, no aprendido). No es un sitio del anillo, pero es un
   "dónde mirar" dado, y lo declaro como límite de lo que se puede decir.

---

## 9. HUMO (se escribe después; §0–§8 no se tocan)

### 9.0 Identidad: **33/33** (`identidad_v5_salida.txt`, un proceso, 474 s)
Primer intento **31/33** (`identidad_v5_salida_intento1_31de33.txt`): los dos casos de inercia (n, n2) comparaban
también la clave `v5`, que es el **eco de la perilla** (0 contra 1) y difiere por construcción. Error del arnés,
no del instrumento; se corrigió saltando esa clave (una línea, declarada en el código) y se repitió entero:
33/33. Con `v5 = 0`: ≡ `organismo_familias_bav` en 17 casos (incluidos PAR, baraja, canal en tres modos y el
ancla de 120 000), ≡ `organismo_v14` (TRONCO) y ≡ `organismo_v15f_on`. Tres controles que deben diferir, 2/2 o
3/3. Mecanismo (T = 60 000, semillas 1 y 2): la hermana lee **−9.0 y −1.0** justo después del mensaje con V-5,
contra **−1.0 y +2.0** con BA-v; el referente lee +3.0 en los dos. **Dato de mecanismo que no predije:** V-5 parte
casillas **muchísimo por la experiencia propia**: 405 partos por bocado y ~424 subcasillas a T = 60 000 (de 2 112
posibles), porque familias de valor opuesto comparten bins en las celdas de forma. No se toca nada por esto.

### 9.1 Coste declarado
UN proceso, sin Pool: **1 emisor + 5 receptores = 6 corridas de 100 000 pasos**, 72 s de pared, semilla **25791**.
Había dos Pools de 6 del coordinador corriendo; no se tocaron.

### 9.2 Números (`datos/humo/humo_v5_20260923_155242.{log,json}`; crudo `humo_v5_20260923_155242_crudo.json`, `710e201cf3490025`)
Montaje: emisor 1/1 (`T1v2`, R = +1.0, t = 42 635); **regla 14: 33 campos IDÉNTICOS** al bloque 6; entrega
t ≈ 66 700; la boca leyó por la vía LENTA en las 5 corridas.

| celda · brazo | comió X | dist | lee(ref) | lee(hermana) tras el mensaje | 1.a exposición de la hermana | muertes | partos msg/bocado |
|---|---|---|---|---|---|---|---|
| **BA-v5 · CANAL** | **1** | — | +3.0 (3/3, 3/3) | — | — | 86 | 45 / 344 |
| **BA-v5 · PAR** | 1 | **1** | +3.0 | **−9.0** | valor −9.0, **no mordió** | 81 | 45 / 295 |
| BA-v5 · BAR-T | **0** | — | −9.0 | — | — | 96 | 36 / 367 |
| BA-v5-sh · CANAL | **0** | — | −5.0 | — | — | 113 | 40 / 289 |
| **BA-v · PAR** (misma semilla) | 1 | **0** | +3.0 | **+3.0** | valor +3.0, **mordió** | 34 | — |

Con n = 1 **no es evidencia de ninguna puerta**. Lo que sí muestra es el **mecanismo en el sitio exacto**: en la
misma semilla, BA-v le presta +3.0 a la hermana y la muerde; V-5 la deja en −9.0 y no la muerde.

### 9.3 Aviso escrito ANTES de la serie (no cambia ninguna letra)
**R6 es la puerta con más riesgo, más de lo que firmé en §5.** En esta semilla BA-v5 muere 81–96 contra 34 de
BA-v, y come menos (3 631–4 056 bocados de comida contra 5 616): el mismo patrón de "abstinencia" que mató a
BA-vm. Mi predicción K4 (BA-v5/BA-v = 1.0×, 0.7–1.5×) queda **en riesgo alto** con n = 1 (2.4× aquí), y la de
P7 (1.2×, 0.8–2.0×) también. No recalibro nada: si P7 cae en las dos series, el veredicto es el de §7 y la frase
de §8 (3) "separa y vive peor".
