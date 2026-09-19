# PREREGISTRO — BLOQUE 5: **VARIAS GANADORAS** — que la referencia baje de la familia a la variante (H-4 de la sala 4; E-7)

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales, sin
retropropagación, que aprende, desaprende, generaliza, sobrevive y **se comunica con referencia**. Hoy: **que el
mensaje baje de la familia a la variante**.

- **Creador:** el creador del candidato "varias ganadoras" (H-4, sala 4). No corre `Pool` (regla 3): entrega
  instrumento + arnés + runner + humo de un proceso.
- **Instrumento:** `organismo_familias_b5.py` (`e0b6b90f6f92d5c1`), construido **por anclas** desde
  `organismo_familias_b4b.py` (`b3dd1d7e66a2d147`) con `construye_familias_b5.py`. Arnés
  `identidad_familias_b5.py`.
- **Runner:** `corre_familias_b5.py`. **Semillas 681–700 y réplica 701–720.** Sólo dirección (−) (ERR-53).
- **Escrito ANTES de correr un solo brazo de la serie.** Las §1–§8 no se tocan después de ver datos; lo que se
  mide se escribe en §9 (humo) y §10 (serie).

---

## 0. **E-7 — el error que este bloque ataca, con su evidencia**

`registro/investigacion/sala4_evolucion/SALA4_evolucion_20260918.md` §B E-7 ("el techo de 2 bits") y §C H-4.

La vía lenta de v15f lee por **UNA** celda ganadora = **un par de píxeles** = **2 bits**, y con 32 estímulos esa
casilla agrupa **12 de los 32** (`n_mismo_bin` mediana, medida en las series 641–660 y 661–680). Consecuencias ya
medidas, seis series seguidas:

| medida (dirección −, `com` = comió a la 1.ª exposición de su vida) | 641–660 | 661–680 |
|---|---|---|
| CANAL− (patrón de X + R cruda) | 17/18 | 16/19 |
| CORTADO− (gemelo mudo) | 2/18 | 0/19 |
| **BAR-T− (patrón de OTRO token)** | **9/18** | **6/19** |
| BAR-H− (patrón de una hermana) | 15/18 | 13/19 |
| VALOR− (sin referencia) | 5/18 | 4/19 |
| PAR− `dist` / su gemelo PAR0− | 11/18 · 4/18 | 6/19 · 7/19 |
| la ganadora usa un píxel VARIABLE, antes del mensaje | 1/18 | 1/19 |

Por eso el bloque 4b **no pudo declarar** "comunicación con referencia": *el mensaje con el patrón de otro token
arrastra la mitad del efecto*. El registro escribió el remedio en el bloque 3: *"el siguiente candidato necesita
**varias ganadoras o compuerta contra la lineal**"*. Este bloque **elige varias ganadoras**, y dice por qué
(§3.3).

---

## 1. La pregunta

Con el mundo, el canal y el emisor **idénticos** a los del bloque 4b, y cambiando **sólo cuántas celdas lee la vía
lenta del receptor**:

1. ¿Cae **BAR-T−** a ≤ CORTADO + 3? (la referencia deja de repartirse entre familias que comparten casilla)
2. ¿Cae **BAR-H−** a ≤ CORTADO + 5? (la referencia baja **a la variante**)
3. ¿Sigue **CANAL− ≥ 15/20**? (el candidato no puede romper el mensaje para ganar especificidad)
4. ¿Trata el receptor **distinto** a X y a su hermana cuando ve a las dos (brazo PAR, `dist` ≥ 12/20)?

---

## 2. LO QUE NO CAMBIA

- **El mundo**: el del bloque 4b, objeto importado (ERR-31), no recopiado: `MUNDO`, `KW_E`, `KW_R` de
  `corre_familias_b4b.py`. D = 12 (9 forma + 3 variable), F = 8 tokens, V = 3 variantes, 32 estímulos,
  `n_exc = 2`, `exc_fija = 2`, `cambio` fuera del horizonte, `vira = 0`, renovación simétrica.
- **El canal**: mismos modos (`emite` / `sen` / `inm` / `mudo`), misma entrega por señalamiento, misma escritura
  del mensaje como **exposición sin consecuencia** en la tabla de pares. **No se toca ni una línea.**
- **El emisor**: `voraz = 1.0` (ERR-51), fijado en el bloque 4b y no recalibrado aquí (§4.2).
- **La escritura de la tabla**: las 66 celdas siguen escribiendo **R crudo por sobrescritura**, y el error propio
  por celda sigue siendo el de su casilla sola. `k_ganadoras` **no toca el aprendizaje**: con `puerta = 3` la vía
  lenta no entra en ningún error (`dlt = R − _wf`, `_ds = R − _lbv`). **Cambia lo que lee la boca, y nada más.**
- **La letra del receptor** del 4b: CANAL ≥ 15/20 contra CORTADO ≤ 5/20, y las puertas por dirección de ERR-53.

---

## 3. LO QUE CAMBIA — **una** perilla, inerte por defecto

### 3.1 `k_ganadoras` (default 1)

Cuántas celdas **lee** la vía lenta. La lectura de la tabla pasa de **una** casilla a la **SUMA de las casillas
CONOCIDAS de las k celdas de menor error propio**, con **abstención** (relevo a la lectura lineal) si **ninguna**
de las k conoce la combinación — exactamente el relevo de v15f/b3/b4/b4b.

**Orden de las k (decisión declarada aquí, antes de medir):** la **primera** es `_MGv`, la ganadora de b4b,
calculada con **la misma línea** y **el mismo desempate al azar** (por eso el consumo del rng no cambia); las
k − 1 restantes salen de ordenar el resto por **(error propio, índice)** — desempate **determinista por índice**,
que no toca el rng. Es lo que hace que **k = 1 sea b4b bit a bit**: el camino `k <= 1` de `_tabla_v15f` son
**literalmente las tres líneas de b4b**.

**k = 1 es el CONTROL DE OCCAM, no un competidor** (SALA2 C.3): es el organismo del bloque 4b, corrido con
semillas nuevas. Si el bloque no reproduce en k = 1 los números de las series 641–680, el problema es el montaje,
no la perilla.

### 3.2 **SUMA, no voto** — decisión escrita antes de medir, con su razón

1. **La tabla guarda R CRUDO.** Ese es el punto de v15f: la boca lee el **valor real** (+1 comida, −3 veneno), no
   un signo. Un voto tendría que **inventar** una magnitud; la suma conserva la unidad de R.
2. **La boca ya satura, así que k no infla la decisión cuando las celdas coinciden.**
   `Vb = 1.2·w + 2·hambre + 0.5 + voraz`, `pb = σ(Vb/0.3)`. Con w = +1 y hambre = 0: `Vb/0.3 = 5.67 → pb = 0.997`.
   Con w = −3: `Vb/0.3 = −10.3 → pb = 3·10⁻⁵`. Ya con **una** celda la sigmoide está saturada. Multiplicar por k
   **no cambia** la decisión en el caso en que las k coinciden: la suma sólo actúa en el caso **mixto**, que es
   exactamente el que discrimina.
3. **En el caso mixto la suma usa la asimetría del mundo** (+1 contra −3): **una** celda que sí distingue cancela
   **tres** que no. Un mensaje que sólo llega a medias **no** hace comer. Es el sesgo conservador que se quiere, y
   el que hace caer a BAR-T.
4. **La suma no necesita desempate** → no consume rng → la identidad con k = 1 es limpia.
   *(Con k ≤ 5 la suma vive en [−15, +5]: `np.exp` no desborda. Sólo el caso estructural del arnés con k = 66
   produce un `RuntimeWarning: overflow in exp`, que da `pb = 0` y no afecta a ningún brazo del bloque.)*

### 3.3 **La alternativa que se DESCARTA: compuerta contra la lineal** (leer la tabla sólo si su error propio < el de la lineal)

Se descarta, por escrito y antes de medir, por tres razones:

- **(a) Pide estado nuevo.** Haría falta una EMA del error propio de la lectura **lineal**, que hoy no existe, más
  su constante. Más maquinaria que la perilla elegida: contra Occam.
- **(b) NO ataca E-7.** La compuerta decide **si** se lee la tabla, no **qué resuelve** la tabla. La fuga de BAR-T
  ocurre **dentro** de la casilla ganadora: el patrón de otro token cae en la misma casilla que el referente, y
  una compuerta que deja hablar a la tabla **no distingue T de X**. No puede mover BAR-T ni un punto.
- **(c) k = 1 es un control de Occam gratis** (b4b bit a bit); la compuerta no tiene ese control gratis.

Queda anotada como candidata para **otro** cuello — *cuando la tabla habla de lo que no sabe* — no para éste.

### 3.4 Arnés `identidad_familias_b5.py`: **106/106** (§9.0)

Apagado ≡ b4b en 13 escenarios × 3 semillas + los tres modos del canal; rng no consumido a T = 120 000; cadena
completa hasta b4, b3, b2, `organismo_familias`, `organismo_v14` (TRONCO) y `organismo_v15f_on`; **inercia** (con
`memoria_pares = None` la perilla no existe para ningún k); **estructura** (la 1.ª de las k es la de b4b, son k
sin repetir, con k > 66 son las 66); cinco `k` mal escritas que **lanzan**; el montaje E → R con las puertas P-I3
y P-I4 comprobadas **por k**; y **cuatro controles que DEBEN fallar**.

---

## 4. BRAZOS, EMISOR Y SEMILLAS

### 4.1 Brazos — los nueve del 4b (−) × k ∈ {1, 3, 5} = **27**

| brazo | qué es | gemelo (P-I3) |
|---|---|---|
| `CANAL-k` | patrón de X + R cruda, entrega por señalamiento | `CORTADO-k` |
| `CORTADO-k` | gemelo **mudo**: hace todo menos escribir el mensaje | — |
| `BAR-H-k` | patrón de una **hermana** de X (T1v0) | `CORTADO-k` |
| `BAR-T-k` | patrón de **otro token** de la misma clase de valencia (T3v2) | `CORTADO-k` |
| `VALOR-k` | sin referencia (patrón de ceros), misma R | `CORTADO-k` |
| `INM-k` | entrega **inmediata** en vez de señalamiento | `CORTADO-k` (prefijo hasta `t_msg`) |
| `OTRO-k` | R-SIN-SAL: el receptor vive en otro mundo | **excluido de P-I3** (ERR-52) |
| `PAR-k` | el receptor ve **X y su hermana** tras el mensaje (`par_herm = (1,0)`) | `PAR0-k` |
| `PAR0-k` | gemelo mudo del brazo PAR | — |

### 4.2 **El emisor NO cambia** (decisión declarada)

Un solo emisor por semilla: **b5 con `k_ganadoras = 1`**, o sea `organismo_familias_b4b` bit a bit, con
`voraz = 1.0`. Su mensaje es **el mismo objeto** en los tres brazos k. Razón: lo que este bloque mide es **la
lectura**, no el habla; si el emisor también cambiara con k, P-I2 y el propio mensaje dejarían de ser
comparables entre brazos y no se sabría qué movió el número. Lo comprueba el caso **(L)** del arnés (el mensaje
de b5/k=1 es carácter a carácter el de b4b).

### 4.3 Semillas y coste

**681–700** y **réplica 701–720** (regla 12). Por serie: 27 brazos × 20 + 20 emisores = **560 corridas** de
100 000 pasos, más 27 de identidad y 20 de diagnóstico estructural (T = 0). `Pool` **sólo el coordinador**.

---

## 5. LAS MEDIDAS — **todo por conducta de la boca** (ERR-44)

### 5.1 La convención

`com` = **la boca MORDIÓ en la primera exposición de su vida al referente** = `n − evX_n`. Es el número que el
registro imprime desde el bloque 4. En la dirección (−) el referente `T1v2` es **comida** dentro de una familia
de **veneno**: el receptor no lo muerde nunca por su cuenta (`CORTADO−` lo confirma corrida a corrida), así que
`com` mide exactamente *"actuó porque otro se lo dijo"*.

### 5.2 Puertas (ERR-53, por dirección; si caen, no se lee nada más)

- **P-I2** — hay mensaje: el emisor voraz anota `T1v2` con R > 0 en **≥ 18/20**, y `t_msg < 2·deriva(R)`. Las
  semillas sin mensaje se **excluyen** y se reportan al lado (regla 10).
- **P-I3** — gemelo, **por k**: cada brazo `sen` comparte con su gemelo el prefijo **exacto** de `log` hasta la
  entrega, en ≥ 18/20 (INM hasta `t_msg`; **OTRO excluido**, ERR-52).
- **P-I4** — nunca visto, **por k**: en `CORTADO-k` la primera exposición de la vida al referente coincide con el
  paso de la entrega, **20/20**.
- **P-I5** — vía por la que se lee, **por k**: la boca usa la vía **lenta** (`fam1 = 0`) en ≥ 18/20. Las semillas
  en que el referente ya le resulta familiar se reportan aparte.

### 5.3 Diagnósticos — observados, **no prometidos**

`n_mismo_bin_k` (cuántos de los 32 estímulos caen en **LAS k** casillas del mensaje), `n_mismo_bin` (la de una
sola casilla, para comparar con b4b), `k_var_pre` / `k_var_post` (cuántas de las k usan un píxel **variable**),
`comH`, `evU` / `okU` (las 6 variantes de control, ninguna de las dos excepciones), `lag_t` / `lag_m` / `lag_par`,
muertes, celdas, divisiones.

### 5.4 Cálculo **estructural** (T = 0, sin simular; `estructura_k` en el runner)

De las 66 celdas, en cuántas **no** se distingue el referente del patrón de cada barajado. Calculado sobre el
catálogo del bloque 0 para las semillas del bloque, **antes** de simular:

| | todas (66) | sólo las de FORMA (36) |
|---|---|---|
| BAR-T (otro token) | 0.424 (rango 0.227–0.682) | **0.278** (0.083–0.583) |
| **BAR-H (la hermana)** | 0.682 (idéntico en las 20) | **1.000 en las 20 semillas** |
| VALOR (ceros) | 0.424 | 0.417 |
| **piso de la intersección si las k ganadoras son todas de forma** | | **4 de 32 — exactamente la FAMILIA** |

**Esto decide el bloque antes de correrlo, y por eso va escrito aquí:** dos hermanas se separan **sólo** en los 3
píxeles de variable, así que **ninguna** celda de forma las distingue. Si el top-k sigue siendo de forma — y en
b4b lo era en 17/18 y 18/19 semillas — **BAR-H no puede caer por muchas k que se añadan**, y la intersección de
las k casillas no puede bajar de 4: el token y sus tres variantes, o sea **la familia**.

### 5.5 Declaración de contaminación

Las semillas **1 y 2** se usaron en el humo (§9) y en el arnés. Ninguna pertenece a 681–720. Los números del humo
**no son evidencia** (n ≤ 2, semillas vistas) y no mueven ningún umbral.

---

## 6. LA LETRA Y LAS PREDICCIONES (escritas antes de correr un solo brazo de la serie)

### 6.1 Umbrales — **por k**, sobre `com`

| | criterio | pasa si |
|---|---|---|
| **R1** | el canal sigue intacto | `CANAL-k ≥ 15/20` **y** `CORTADO-k ≤ 5/20` **y** pareado (CANAL come y CORTADO no) ≥ 14/20 |
| **R2** | **la que decide** — otro token | `BAR-T-k ≤ CORTADO-k + 3` |
| **R3** | la hermana — **la variante** | `BAR-H-k ≤ CORTADO-k + 5` |
| **R4** | hace falta el campo de referencia | `VALOR-k ≤ CORTADO-k + 3` |
| **R5** | especificidad entre hermanas (brazo PAR) | `dist ≥ 12/20` **y** `dist(PAR-k) ≥ dist(PAR0-k) + 5` |
| **R6** | el candidato no cuesta el organismo | muertes(CANAL-k) ≤ 1.5 × muertes(CANAL-k1) **y** okU(CANAL-k) ≥ okU(CANAL-k1) − 0.10 |

**Se declara** en una k sólo si pasan las cuatro puertas **y** R1, R2, R3 y R4 en esa k, **en las dos series**.
R5 y R6 se reportan siempre; R6 puede matar al candidato aunque R1–R4 pasen (§8).

### 6.2 Predicción numérica, por k (mediana / rango esperado sobre 20 semillas)

| medida (`com`) | **k = 1** (control de Occam) | **k = 3** | **k = 5** |
|---|---|---|---|
| CANAL− | 15–19 | 15–19 | 14–19 |
| CORTADO− | 0–3 | 0–3 | 0–3 |
| **BAR-T−** | **7–10** (R2 **cae**, es b4b) | **1–4** (R2 **pasa**) | **1–5** (R2 **pasa**) |
| **BAR-H−** | **12–17** (R3 cae) | **11–17** (R3 **cae**) | **10–18** (R3 **cae**) |
| VALOR− | 3–6 | 0–3 | 0–3 |
| PAR− `dist` (gemelo PAR0−) | 5–12 (3–8) | 5–13 (3–8) | 5–13 (3–8) |
| `n_mismo_bin_k` (de 32) | **12** | 4–8 | **4–6**, nunca < 4 |
| celdas del top-k con píxel variable | 0 (mediana) | 0–1 | 0–1 |
| P-I5 vía lenta | ≥ 18 | ≥ 18 | ≥ 18 |
| muertes (mediana) | 27–55 | ≤ 1.3 × k=1 | ≤ 1.3 × k=1 |

**La aritmética de la que salen esos números**, escrita antes: la boca come si la suma leída supera ≈ −1
(`1.2·w + 2·hambre + 0.5 > 0` con hambre ≈ 0.3). Si m de las k celdas traen el mensaje (+1) y las k − m restantes
traen lo que la familia dejó en la casilla de X (−3, porque T1 es familia de veneno y todos sus miembros comparten
los bins de forma), la suma es `4m − 3k`, y come si **m > (3k − 1)/4**: con k = 1 basta **una** celda que colisione;
con k = 3 hacen falta **las tres**; con k = 5, **cuatro de cinco**. Con la tasa de colisión de BAR-T observada en
b4b (≈ 0.42 condicionada a ser la ganadora; 0.278 estructural) eso da ≈ 0.07–0.15 para k = 3 y ≈ 0.11–0.20 para
k = 5.

**Predicción no obvia que me la juega:** *k = 5 **no** será mejor que k = 3 en BAR-T*, porque con la asimetría
+1/−3 una sola celda discriminante cancela tres colisionantes, y con k = 5 cuatro colisionantes todavía ganan a
una discriminante. Si k = 5 sale claramente por debajo de k = 3 (≥ 4 puntos), mi aritmética está mal.

### 6.3 Qué me refuta

1. **Si BAR-T− NO baja con k = 5** (sigue > CORTADO + 3 en las dos series): **el techo no era de bits**. La
   referencia está en la **retina** — los 3 píxeles de variable — y la línea pasa al **mundo**, no al organismo
   (E-7 y la cláusula de refutación de H-4). Es la refutación principal y la escribo primero.
2. **Si BAR-H− SÍ baja** a ≤ CORTADO + 5: mi cálculo estructural de §5.4 (100 % de las celdas de forma son ciegas
   a la hermana) es irrelevante porque el top-k se puebla de celdas variables tras el mensaje — y entonces la
   referencia **sí** baja a la variante y el objetivo del encargo se cumple. Lo predigo que NO, y me alegraría
   equivocarme: sería el resultado fuerte.
3. **Si CANAL− cae por debajo de 15/20 con k > 1**: la suma rompe el mensaje. No debería pasar (en la entrega el
   mensaje sobrescribe la casilla de X en **las 66** celdas y `lag_m = 0`), y si pasa, el candidato muere.
4. **Si R6 cae** (muertes > 1.5× o okU cae > 0.10): la perilla no es quirúrgica y el precio se paga fuera de la
   medida que interesa.
5. **Si k = 1 no reproduce los números de b4b** (CANAL 15–19, BAR-T 6–10, BAR-H 12–17): es el montaje, no la
   perilla, y se para.

### 6.4 Lo que predigo que pasará, en una frase

**BAR-T cae, BAR-H no.** La referencia baja **del vecindario de casilla a la FAMILIA** — y ahí se para, en el
piso estructural de 4 de 32 —, así que **nada se declarará por la letra de §6.1** (R3 cae en las tres k) y el
resultado útil será haber **medido dónde está el cuello de verdad**: no en los bits de la memoria, sino en que el
mundo no le da al organismo ninguna razón para mirar los píxeles que separan a dos hermanas.

---

## 7. LO ÚNICO QUE SE PERMITE CORREGIR

- Que una puerta de **montaje** (P-I2…P-I5) caiga: se para, se numera un ERR, se corrige el montaje y se corre en
  **semillas nuevas**. Nunca se toca un umbral de §6.
- Que el runner caiga en el análisis: **los datos crudos ya están guardados** (ERR-54) y el veredicto se recalcula
  desde el JSON crudo con un script del repositorio, nunca en línea (regla 10).
- Si una puerta cae por **una** semilla en el borde (k/20 a ±1): réplica automática en un rango nuevo (regla 12).

Nada más. Ni k nuevas, ni suma cambiada por voto después de ver datos, ni umbrales movidos.

---

## 8. QUÉ SE PODRÁ DECLARAR, Y QUÉ NO

- **Se podrá declarar**, si pasan las puertas y R1–R4 en alguna k en **las dos series**:
  *"el mensaje (patrón público + recompensa cruda) cambia la conducta del receptor sin experiencia propia, y su
  referencia es específica del estímulo nombrado frente a otro token."* Con R3 además: *"…y frente a otra variante
  de la misma familia"* — sólo entonces la palabra **variante** entra en el vocabulario (regla 6).
- **No se podrá declarar** nunca en este bloque: "lenguaje", "palabra", "concepto", ni que el organismo
  *entienda* el mensaje. Se declara conducta de la boca en la primera exposición, y nada más.
- **R6 manda sobre todo lo demás**: un candidato que compre especificidad con muertes no entra a ningún sitio,
  aunque R1–R4 pasen. Se reporta y se para.
- **k = 1 no es un brazo que gane**: es el control de Occam. Si ninguna k > 1 mejora a k = 1 en R2, **la perilla
  sobra** y se retira (igual que la tercera necesidad del mundo vivo, 18 sep 09:43).

---

## 9. HUMO — resultado (§1–§8 no se tocaron)

### 9.0 Identidad: **106/106** (arnés completo, un proceso). Subconjunto del runner: **18/18** (9 casos × 2 semillas), incluidos **(K)** y **(C)**, que DEBEN fallar.

### 9.1 Coste declarado del humo (regla 3), y dónde me paso

14 corridas de **30 000** pasos (2 emisores + 6 brazos × 2 semillas) = el trabajo de **4.2** corridas de 100 000.
Por trabajo estoy por debajo del techo de la regla 3; **por número de corridas me paso de 6, y lo declaro**. Un
proceso, sin `Pool`. Semillas 1–2: ninguna de las 681–720 queda expuesta.

### 9.2 La tabla del humo (n = 2, T = 30 000: **NO es evidencia**)

`datos/familias_b5_humo_20260918_192745.json` (`a7154ce5981a2f67`) y su `.log`. Identidad del subconjunto del
runner **18/18** (9 casos × 2 semillas), incluidos **(K)** `k=5 ≠ k=1` y **(C)** `CANAL-k5 ≠ CORTADO-k5`, que
DEBEN fallar. Gemelo (P-I3): prefijos idénticos en k = 1 y en k = 5. **Cruce `cod0` del emisor contra
`escala_codigo` (bloque 0): idéntico campo a campo** — ver la nota de §9.3 sobre por qué en b4/b4b era vacuo.

| brazo | comió a la 1.ª (s1 · s2) | vía | `n_mismo_bin_k` (de 32) | celdas del top-k con píxel variable | muertes | celdas |
|---|---|---|---|---|---|---|
| CANAL-k1 | **1 · 1** | lenta · lenta | 16 · 12 | 1/1 · 0/1 | 7 · 17 | 47 · 47 |
| CORTADO-k1 | 0 · 0 | lenta · lenta | 16 · 12 | 0/1 · 0/1 | 7 · 8 | 48 · 45 |
| BAR-T-k1 | 0 · **1** | lenta · lenta | 16 · 21 | 0/1 · 1/1 | 8 · 12 | 45 · 47 |
| CANAL-k5 | **1 · 1** | lenta · lenta | **6 · 1** | 1/5 · **5/5** | 8 · 20 | 40 · 36 |
| CORTADO-k5 | 0 · 0 | lenta · lenta | 4 · 1 | 0/5 · **5/5** | 9 · **32** | 38 · 34 |
| BAR-T-k5 | **1** · 0 | lenta · lenta | 9 · 1 | 1/5 · **5/5** | 9 · 13 | 49 · 36 |

Diagnóstico estructural (T = 0) de las dos semillas del humo: BAR-T 0.682 / 0.424 (forma 0.583 / 0.278), BAR-H
0.682 en las dos (**forma 1.000 en las dos**), VALOR 0.424, **piso de forma 4/32**.

**Coste y estimación:** 14 corridas de 30 000 pasos, 118 s de pared, un proceso. El runner estima la serie
completa en **560 corridas de 100 000 pasos ≈ 5.2 min** de pared con `Pool(14)`.

### 9.3 Qué dice el humo, sin ajustar nada

1. **El instrumento hace lo que dice.** k = 1 es b4b bit a bit (18/18 + 106/106 del arnés), los gemelos comparten
   prefijo por k, la boca lee la vía **lenta** en las 12 corridas, y `lag_m = 0` en todas: el mensaje se escribe y
   se lee en el mismo paso, así que el candidato no puede ganar por olvido.
2. **La resolución baja mucho más de lo que predije.** `n_mismo_bin_k` cae de 16/12 (k = 1) a **6/1** (k = 5), o
   sea **por debajo del piso de 4** que §5.4 fija para un top-k todo de forma. La razón está a la vista y es la
   que §5.4 nombraba como única salida: **en la semilla 2 las cinco ganadoras contienen el píxel 11**, el píxel
   variable del referente. O sea: **con k = 5 la tabla sí mira la dimensión que separa a dos hermanas.**
   Eso pone en riesgo mi predicción de §6.2 (`k_var_post` mediana 0–1) y abre la refutación nº 2 de §6.3 — que
   BAR-H caiga. **No toco §6: las predicciones se quedan como están escritas y que las tumbe la serie.**
   *(Estos números del arnés y del humo se vieron DESPUÉS de escribir §1–§8; el diagnóstico del arnés que los
   mostraba lanzó una excepción en la primera pasada y se leyó cuando §6 ya estaba cerrada.)*
3. **El aviso que puede matar al candidato es R6, no R1.** CANAL− come a la primera en 2/2 con k = 1 y con k = 5,
   y CORTADO− en 0/2: el canal no se rompe. Pero con k = 5 las **muertes suben** (CORTADO−: 32 contra 8 en la
   semilla 2) y las **celdas bajan** (36–40 contra 45–48). Con n = 2 eso no es nada; con 20 semillas, R6 es el
   criterio que puede tumbarlo, y está escrito desde §6.1.
4. **Defecto encontrado en el instrumento heredado (candidato a ERR, no corregido aguas arriba).**
   `CF.cruza_cod0` **salta toda fila cuyo `mundo` sea `None` o `'AB'`**, y en `corre_familias_b4.py` y
   `corre_familias_b4b.py` las filas del emisor se construyen como `dict(tipo='R', seed=s, cod0=...)`, **sin el
   campo `mundo`**: el cruce que el log declara "IDENTICO campo a campo" **no comparó nada** en los bloques 4, 4b
   y las dos series de la dirección (−). Consecuencia probable: ninguna (el mismo cruce sí corre de verdad en b2
   y b3, sobre el mismo mundo), pero es una comprobación que se creía hecha y no lo estaba. En
   `corre_familias_b5.py` la fila lleva `mundo='familias'` y el cruce **sí** se ejecuta. El coordinador decide si
   esto lleva número de ERR.
5. **Lo que el humo NO dice:** nada sobre BAR-T ni BAR-H (n = 2, semillas vistas, T = 30 000 contra 100 000 del
   bloque). BAR-T-k1 comió 1 de 2 y BAR-T-k5 también 1 de 2: con dos semillas no se distingue de una moneda.

---

## 10. SERIE 681–700 y RÉPLICA 701–720 — resultado

*(lo rellena el coordinador tras correr el `Pool`)*

## ERR-63 (coordinador, 18 sep 19:50; numeracion del hallazgo del creador): en corre_familias_b4.py y corre_familias_b4b.py las filas del emisor pasadas a cruza_cod0 no llevaban el campo mundo, y el cruce saltaba todas las filas: el 'IDENTICO campo a campo' de los bloques 4 y 4b no comparo nada. Consecuencia probable nula (el mismo cruce si corre en b2/b3 con el mismo codigo). En b5 la fila lleva mundo='familias' y el cruce se ejecuta.
