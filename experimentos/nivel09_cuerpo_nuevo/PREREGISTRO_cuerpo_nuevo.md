# PREREGISTRO — FASE 9, BLOQUE 1: el cuerpo nuevo. ¿Aprende en MENOS DE UNA VIDA lo que su linaje ya sabe?

**Misión (primero, siempre): llegar a la AGI por este camino** — organismo mínimo, reglas locales, sin
retropropagación, peldaños preregistrados con controles y réplicas. **Hoy:** H-1 dejó escrito (ERR-62) que con
muerte real *ningún* modo de herencia sostiene el linaje (R₀ 0.14–0.17 contra 0.87–0.98 del inmortal subsidiado), y
diagnosticó por qué: **"el hijo nace vacío y muere antes de aprender"**. La fase 9 prueba lo único que queda sin
herencia lamarckiana de pesos: que el recién nacido **lea el nodo del linaje por relevancia y desde su primer paso**.

**Del creador para el coordinador, 21-sep-2026, escrito ANTES del humo** (§8 trae las predicciones del humo y §10 su
resultado). **Semillas NUEVAS: 1501–1520 (serie) y 1521–1540 (réplica, regla 12).** Ninguna cifra de H-1, del bloque 2
ni del BLOQUE ALMA se recalibra: aparecen aquí sólo como **origen declarado de los márgenes**.

---

## 0. El hecho, y la enmienda a la propuesta del director sobre las semillas

**Semillas: 1001–1020 / 1021–1040 NO se pueden usar.** El director propuso ese rango y pidió confirmarlo con `grep`.
La confirmación lo **refuta**: `experimentos/etapa4_v9/corre_etapa4_v9.py` líneas 57, 71 y 73 corren la cría del bloque
H con **`1000 + seed`** para `seed` 1..20 → **1001–1020 ya está usado** (día 4, `etapa4_v9_20260916_170519`;
`PREREGISTRO_etapa4_v9.md` §"Cría"). Además 1101–1140 están **reservadas** por `sala2/DISENO_crece_codigo.md` (con un
cálculo estructural ya guardado, `coactividad_tren_xor01_s1101-1140.json`) y 1201–1400 por los diagnósticos de
`sala2/diagnostico_familias4.py` y `diagnostico_mundo.py`. **Se propone 1501–1520 y réplica 1521–1540**, verificadas
libres: `grep` sobre `*.py` y `*.md` de `experimentos/`, `registro/` y `organismo/` no devuelve ninguna aparición como
semilla, y el barrido de todos los JSON de `datos/` (562 archivos, claves `sem*`/`seed*`) da **máximo 944**.

**Lo que este bloque NO es.** No es un candidato al tronco: `CRITERIO_TRONCO_v2.md` no aplica. Mide un **mecanismo** en
el mundo vivo. Por eso la cadena de anclas se queda en **v14.1** (no v14.2): todo el mundo vivo — bloque 2, H-1, ALMA —
está medido sobre v14.1 y el brazo NADA **tiene** que reproducir NADA_CM de H-1 para que las predicciones tengan ancla.
B-5 (v14.2) repara el alias de código y movería esa línea base. Se declara y se dice.

---

## 1. Hipótesis

**H-F9.** Un cuerpo recién nacido, vacío, que lee el nodo de su linaje **eligiendo los mensajes por relevancia local**
(el delta que la vía lenta le aplicaría **ahora**, recalculado tras cada mensaje) y **desde su primer paso**,
(a) rechaza lo que mata a su linaje **en su primer encuentro** — es decir, aprende en **cero** pasos lo que al fundador
le costó 2–3 mordidas y la vida —, (b) vive varias veces más, y (c) eso **sube R₀ y r** frente a H-1.
**Y la conexión no es un premio: el contenido tiene que ser el correcto** (nodo barajado ≈ nada) **y el ranking tiene
que estar vivo** (un ranking congelado produce miedo a todo, no conocimiento).

**Memoria nueva: CERO.** El nodo ya existía (BLOQUE ALMA). La relevancia es una función de lo que ya hay
(`|R − (Wps−Wns)·P|`, el mismo delta de la regla lenta) que **se calcula y se tira**. La conexión desde el nacimiento
es una perilla que ya existía (`conectado`). No hay estructura, tabla ni vector nuevos.

---

## 2. El instrumento y las anclas

**`organismo_f9.py`**, construido POR ANCLAS (11 inserciones) por **`construye_f9.py`** desde
**`organismo_alma2.py` (`4fd616aeaf535e61`)**, que aquí **sólo se lee**. Cadena verificada por sha en el constructor:
`organismo_alma` (`7c09cec391daa879`) ← `organismo_vivo_h1` (`9e99ff87b5e2db1e`) ← `organismo_vivo_rep2`
(`96feb4918dc5d694`) ← `organismo_vivo_rep` (`aa823d56c2d4213c`) ← `organismo_vivo` (`20c0961c79de8825`) ←
**TRONCO CONGELADO `organismo/organismo_v14.py` v14.1 (`feefc88b1fd8d434`)**. Ningún archivo existente se toca
(regla 1). Todo lo nuevo vive en `experimentos/nivel09_cuerpo_nuevo/`.

| perilla | qué hace |
|---|---|
| **`nodo_rel=0`** | **el ancla: `organismo_alma2` BIT A BIT**. Lectura por **recencia** (los últimos `nodo_lee`) |
| **`nodo_rel=1`** | **RELEVANCIA VIVA (el candidato).** Alcance = **todo** el nodo. Puntaje = `|R − (Wps−Wns)·P|` con el vector **del propio lector**, **recalculado después de cada mensaje absorbido**; empate por recencia. *Relevante = lo que más me cambiaría ahora*: en cuanto aprendió el veneno, el veneno deja de ser relevante y pasa a serlo la comida. **No guarda nada** |
| **`nodo_rel=3`** | **RELEVANCIA FIJA (control).** El mismo puntaje calculado **una sola vez**, con el vector del recién nacido (que es 0) → el ranking degenera en `|R|` y lee casi sólo veneno (−3 contra +1). Es la **trampa 2 en carne propia** |
| **`nodo_rel=2`** | **CONTROL DE ACCESO.** Mismo alcance (todo el nodo), selección **al azar**, rng propio `SEM_REL(seed) = 870000 + 1000000·seed` (no toca el rng del mundo, ni el de los hijos `700000+`, ni el de la herencia barajada `800000+`, ni el del alma al azar `850000+`, ni el del barajado del nodo `860000+`; ERR-60). Separa **rankear** de **no expirar** |
| **`nodo_baraja=1`** (ya existía) | las recompensas de los mensajes se permutan entre sí: **mismas marginales, asociación destruida**. Se aplica **después** de la selección: REL_BAR lee el mismo procedimiento sobre contenido mal emparejado |
| **`con_desde=c`** | el linaje se conecta recién tras la muerte `c` (los cuerpos 1..c−1 son **exactamente NADA**). Es "nacimiento sin conexión" convertido en brazo que **puede fallar**, con su propia línea base dentro del mismo brazo y la misma semilla |
| **`rep_acum=1`** | **reproducción desacoplada de la saciedad, PERILLA APARTE** (detrás de `rep_mide`, **no** del alma: vale también con `alma=None`). La ventana cuenta pasos saciados **sin exigir que sean seguidos**. **Se reinicia AL MORIR**: la acumulación es *dentro de un cuerpo*; el recién nacido **no** hereda el avance de su padre (si lo heredara, sería un regalo encubierto y R₀ dejaría de ser honesto). Sin memoria nueva: reusa `_gv` |
| **`f9=1`** | medidas de **solo lectura** del cuerpo que muere: `p1`, `c1`, `t_ok`, `con_cuerpo` |

**El alma NULA.** La fase 9 **no tiene alma**: `alma = curita_f` (siempre `(f)`, `menu='f'`), de modo que el
instrumento **no puede** mover dote, umbral ni herencia. El nodo y la conexión son **mecanismo**, no curita elegida.
El arnés comprueba que ese brazo es `organismo_alma2` con `alma=None` **bit a bit** (caso C1/C2): la línea base de la
fase 9 **es** NADA_CM de H-1.

---

## 3. Brazos y semillas

**Cuerpo común:** `CUELLO_MIN` (`rep_cuello=2`) + `MED2` + `h1=1` + `muerte_real=1` + `dote=0.6` + `rep_X=500`,
`rep_umbral=1.0`, `rep_coste=0`, `rep2_regalo=600`, `nodo_k=20`, `nodo_lee=50`. **Es el mismo cuerpo, constante por
constante, en el que H-1 midió R₀ 0.148/0.140 (NADA) y 0.160/0.170 (M1) y ALMA midió NINGUNA/CIEGO/BARAJA** (regla 14:
la entrada se compara campo a campo; el arnés lo hace por identidad, no "por defecto").

| brazo | perillas | papel |
|---|---|---|
| **RENACE** | `muerte_real=0`, sin alma | **ancla con sha**: la muerte de hoy. Si no reproduce el bloque 2, **no se lee nada** |
| **NADA** | `nodo=0, conectado=0, hereda='nada'` | la línea base = NADA_CM de H-1. *"linaje sin nodo"* |
| **M1** | `nodo=0, hereda='M1'` | *"linaje sin nodo"* **con** la mejor herencia de H-1 (el vector) |
| **REC** | `nodo=1, conectado=1, nodo_rel=0` | el mecanismo de ALMA/CIEGO sin alma: nodo **por recencia** |
| **REL** | `nodo_rel=1` | **EL CANDIDATO** |
| **REL_FIJO** | `nodo_rel=3` | ranking congelado: predicción escrita = evita el veneno y **pierde** en saciedad, comida y R₀ |
| **REL_BAR** | `nodo_rel=1, nodo_baraja=1` | **control de contenido** |
| **REL_AZAR** | `nodo_rel=2` | **control de acceso** |
| **REL_TARDE** | `nodo_rel=1, conectado=0, con_desde=5` | **"nacimiento sin conexión"** |

**Factorial:** 9 brazos × **2 niveles de `rep_acum`** × 20 semillas = **360 corridas** de T = 100 000 por serie.
`rep_acum` es la **perilla del mundo**, no el mecanismo: el veredicto del mecanismo se lee **dentro** de cada nivel.

**Semillas 1501–1520**, réplica **1521–1540**. **Alias estructurales de código, calculados con
`nivel11_mundo_vivo/diagnostico_codigos.py` ANTES de la serie y sin simular nada** (regla 10): en **1501–1520** hay
**una** semilla con solapamiento ≥ 3 — **1508 (`D&B` = sal con veneno)**; en **1521–1540** hay **dos** — **1522
(`D&C` = sal con agua)** y **1525 (`C&B` = agua con veneno)**. Se reporta el conjunto completo y al lado las
**LIMPIAS** con los **mismos** umbrales.

---

## 4. Medidas

Todas de solo lectura, por corrida de 100 000 pasos.

- **`R₀` = descendientes / vidas = desc / (muertes + 1)** — la definición de H-1 (§3 de `PREREGISTRO_h1_muerte.md`),
  no la del instrumento. `R₀ < 1` ⟺ el linaje no se reemplaza.
- **`r` = descendientes − muertes** (la medida validada del bloque 2, ERR-40).
- **vida mediana** por cuerpo (`vidas_h1`, sin tope), partida en fundados / heredados.
- **`p1`** = fracción de cuerpos que **rechazan lo malo para su necesidad activa en su PRIMER encuentro tras nacer**
  (B con hambre, D con sed). **Es la medida de "menos de una vida"**: `p1` alto significa que el cuerpo nuevo no
  necesita morder el veneno para saberlo.
- **`c1`** = fracción que **muerde lo bueno en su primer encuentro** (A con hambre, C con sed).
- **`sac_frac`** = `pasos_viables / T_efectivo` (fracción de pasos con las dos necesidades saciadas).
- **`t_ok`** = pasos **desde su nacimiento** hasta su primera mordida con `R > 0` (*"tiempo hasta la primera comida
  acertada del nacido"*, lo que pidió el director).
- **`exposiciones[A]`**, `muertes_nec`, `fundadores`, `frac_fund`, `lect_div/lecturas`, contabilidad H1-8 entera.

**La trampa 2 (acierto sin balancear), y cómo se cierra.** Un cuerpo que muerde menos sube `p1` **gratis**. Por eso
**`p1` nunca se lee solo**: la puerta exige además que no caiga `c1` y que **no caiga la saciedad** (`sac_frac`), y el
brazo **REL_FIJO** existe justamente para que el modo de fallo se vea medido y no supuesto.
**Dato lateral del arnés (T = 20 000, semilla 1, UN proceso; NO es humo ni evidencia, y ningún umbral se fija con
él):** `c1` sale **1.00** en NADA, REC, REL y REL_FIJO y **0.75** en REL_BAR → `c1` está cerca del techo porque el
hambre empuja a morder; **el balance con dientes lo llevan `sac_frac`, `exposiciones[A]` y `R₀`**, y `c1` queda como
**piso**. Se declara aquí, antes de escribir los umbrales.

**Estadística (ERR-37/61).** `R₀`, `r`, vidas, fracciones y tasas son **integrales de trayectoria** → **A₁₂ sin
parear**, medianas y cuartiles. Ningún `max` sobre lecturas; un `None` nunca cuenta como victoria. Lo único pareado es
la comparación **dentro** de REL_TARDE (cuerpos 1–4 contra ≥ 5 en la misma corrida), que por eso es la más potente.

---

## 5. Predicciones — umbrales escritos ANTES de medir (los diez los imprime el runner, ERR-89)

Salvo indicación, todo en el nivel **`rep_acum = 0`**.

| # | predicción (1501–1520) | de dónde sale | qué la refuta |
|---|---|---|---|
| **F9-1** | **ANCLA, BLOQUEANTE**: mediana `R₀`(NADA) ∈ **[0.10, 0.22]**, vida mediana(NADA) ∈ **[90, 170]**, `R₀`(RENACE) ∈ **[0.70, 1.40]**, `r`(RENACE) ∈ **[−50, +25]** | H-1 ×2 series: R₀ 0.148/0.140, vida 125/119, RENACE 1.03/0.96 y r +3/−2 | si cae, **el instrumento se movió y no se lee nada más** |
| **F9-2** | **el nodo por relevancia alarga la vida**: vida(REL) ≥ **2.5×** vida(NADA) y A₁₂ ≥ **0.85**. Rango esperado de vida(REL): **[300, 900]** | ALMA: CIEGO 594 contra NINGUNA 125 = 4.75× | razón < 2.5 o A₁₂ < 0.85 → leer el nodo no compra vida |
| **F9-3** | **MENOS DE UNA VIDA (la pregunta)**: `p1`(REL) ≥ **0.60** (rango **[0.60, 0.95]**), `p1`(REL) − `p1`(NADA) ≥ **0.30**, A₁₂ ≥ **0.85**, **y el balance**: `c1`(REL) ≥ `c1`(NADA) − 0.10 **y** `sac_frac`(REL) ≥ 0.95× `sac_frac`(NADA) | un cuerpo vacío muerde con `pb ≈ 0.99` (su valor es 0) → `p1`(NADA) ≈ 0.05–0.25; 50 mensajes con `eta_s=0.15` saturan el valor del veneno antes de la 12.ª exposición | `p1`(REL) < 0.60, o el balance cae → **lo que viaja es cautela, no conocimiento** (se dice con ERR) |
| **F9-4** | **contenido, no magnitud**: A₁₂(vida REL > REL_BAR) ≥ **0.80** y `p1`(REL_BAR) ≤ `p1`(NADA) + 0.15 | ALMA: BARAJA 0.175 / vida 226 contra CIEGO 0.275 / 594; H1-4 | REL_BAR ≈ REL → **lo heredable es la magnitud**, ERR y se dice |
| **F9-5** | **relevancia > recencia**: A₁₂(vida REL > REC) ≥ **0.65** y `R₀`(REL) ≥ **1.15 ×** `R₀`(REC) | la hipótesis que dejó el BLOQUE ALMA: *"las lecciones expiraban"* | A₁₂ ≤ 0.55 → **la relevancia no aporta sobre la recencia: el mecanismo es "el nodo", no "la relevancia"**. *Probabilidad que declaro de que esta puerta caiga: ~40 %* |
| **F9-6** | **rankear, no sólo acceder**: A₁₂(vida REL > REL_AZAR) ≥ **0.65** | si sólo importara no expirar, el azar sobre todo el nodo empataría | A₁₂ ≤ 0.55 → lo que paga es **el alcance**, y el mecanismo se renombra *"nodo que no expira"* |
| **F9-7** | **conexión desde el nacimiento**: A₁₂(vida REL > REL_TARDE) ≥ **0.65** **y**, dentro de REL_TARDE, los cuerpos ≥ 5 viven ≥ **2×** los cuerpos 1–4 en ≥ **15/20** semillas | los cuerpos 1–4 son NADA por construcción | el contraste interno < 15/20 → conectarse tarde no cuesta: la conexión no es *desde el nacimiento*, es *conexión y ya* |
| **F9-8** | **reproducción desacoplada (perilla aparte)**: `R₀`(NADA, acum=1) ≥ **1.30 ×** `R₀`(NADA, acum=0) y **Spearman ≥ 0.80** entre el orden de brazos de los dos niveles. **Cláusula H1-6**: se reporta si algún brazo cruza `R₀` ≥ **0.90** con `fundadores` ≤ 2. Predicción de `R₀`(REL, acum=1): **[0.45, 1.10]**; *probabilidad que declaro de cruzar 0.90: ~30 %* | con vida ×3–5 y ventanas acumuladas, el cuello deja de ser "500 pasos seguidos" | si el orden cambia (Spearman < 0.80) → la perilla del mundo **no** es ortogonal al mecanismo y los dos niveles se leen por separado. **Si ningún brazo cruza 0.90 → H-1 y ERR-62 SIGUEN EN PIE y se dice** |
| **F9-9** | **seguridad**: contabilidad H1-8 en **18/18** celdas; `lect_div/lecturas`(REL) ≥ **0.50** (si fuera 0, la perilla es **inerte**: ERR-38); `lect_div`(REC) = **0**; `exposiciones[A]` de cada celda ≥ **0.50 × NADA** — con **REL_FIJO EXENTO y reportado**, porque su hipótesis escrita **es** que come menos: castigarlo ahí confundiría *"el mundo se quedó sin comida"* con *"este brazo eligió no comer"* (declarado aquí, antes de correr) | arnés 88/88 | contabilidad < 18/18 → instrumento, se para. Comida < 0.50× → los cuerpos vacían el anillo y `R₀` se lee neto |
| **F9-10** | **la relevancia viva no es miedo a todo**: `p1`(REL_FIJO) ≥ **0.60** (el ranking congelado **también** evita) **pero** `R₀`(REL) ≥ **1.15 ×** `R₀`(REL_FIJO) y A₁₂(`sac_frac` REL > REL_FIJO) ≥ **0.65** | con W = 0 el ranking degenera en `|R|`: el veneno vale −3 y la comida +1, así que se leen casi sólo venenos | si REL_FIJO iguala o gana → **recalcular la relevancia no aporta** y el mecanismo se simplifica a "leer los mensajes de mayor `|R|`" (sería una simplificación buena, y se declara) |

---

## 6. Las cuatro trampas, y las propias

1. **Canal simétrico** — n/a: el canal es de una sola dirección (el que muere escribe, el que nace lee) y el que lee
   no escribe en su propio nacimiento. Los controles BARAJA / AZAR / TARDE cubren el resto.
2. **Acierto sin balancear** — es **la** trampa de este bloque: `p1` sube gratis si el cuerpo muerde menos. Cerrada
   con la puerta doble de F9-3 (`c1` y `sac_frac`) y con el brazo **REL_FIJO**, que es el modo de fallo **medido**.
3. **El mundo que se come la comida** — más cuerpos ⇒ más consumo del anillo. Acotada por `exposiciones[A]` ≥ 0.50×
   RENACE en F9-9, y **`frac_fund` se reporta**: si REL vive más, se extingue menos, recibe **menos** regalo de
   fundación → la medida se le pone **más difícil**, no más fácil (conservador).
4. **Sitios fijos** — `spawn()` sortea y el recién nacido aparece en `rng.integers(L)`.

**Propias, declaradas:**
(i) **`rep_acum` como regalo encubierto.** Controlada por construcción (se reinicia al morir) y probada en el arnés
(caso G2: ningún descendiente llega antes de 500 pasos del nacimiento de su cuerpo).
(ii) **`t_ok` mide al revés.** *Escrito antes de correr:* el cuerpo vacío muerde lo primero que ve, así que
**`t_ok`(NADA) va a ser MENOR que `t_ok`(REL)**. Eso no refuta nada: muestra que `t_ok` solo **no** mide aprender. Se
reporta siempre y **no es puerta**.
(iii) **`c1` cerca del techo** (§4): se reporta y sirve de piso; el balance lo llevan `sac_frac` y `R₀`.
(iv) **Elegir el brazo mirando el dato**: el factorial completo se corre entero y las diez puertas están escritas aquí;
ningún brazo se añade ni se quita después.
(v) **El nodo crece sin tope** (20 mensajes por muerte). Se reporta `nodo_n`; si la relevancia dependiera del tamaño
del nodo, REL y REC coincidirían al principio (el arnés lo mide: caso F4/F5, con `nodo_lee` enorme REL ≡ REC).

---

## 7. Lo que NO se declara

- **Nada nace.** `descendientes` sigue siendo un contador de ventanas de viabilidad; lo que cambia es que el cuerpo
  siguiente es **otro** individuo. No se dice "población" (hay un cuerpo a la vez), "generación", "selección",
  "evoluciona", "cultura", "enseña", "recuerda su vida pasada", "quiere".
- **No se dice "aprende en menos de una vida" si sólo sube `p1`.** El vocabulario permitido si F9-2, F9-3, F9-4 y F9-9
  pasan es: *"el cuerpo nuevo rechaza en su primer encuentro lo que mató a su linaje, sin dejar de comer"*.
- **`rep_acum` no declara mecanismo**: es una perilla del mundo; un `R₀` alto conseguido ahí vale lo que vale abaratar
  el mundo (lección del BLOQUE ALMA), y se dice.
- 20 semillas no cierran nada: piden la réplica 1521–1540 (regla 12).

---

## 8. Humo (UN proceso, 6 corridas de T = 100 000: NADA, REC, REL × semillas 1 y 2, YA VISTAS) — predicciones ANTES de lanzarlo

- **HH1** vida mediana(REL) > vida mediana(NADA) en 2/2.
- **HH2** `p1`(REL) > `p1`(NADA) en 2/2.
- **HH3** contabilidad H1-8 y longitud de las listas por cuerpo (`len(p1) = len(c1) = len(t_ok) = muertes`) en 6/6.
- **HH4** `lect_div` > 0 en REL (3/3 por semilla) y `lect_div` = 0 en REC.
- **HH5** `c1`(REL) ≥ `c1`(NADA) − 0.10 en 2/2.

**Sólo HH3 y HH4 bloquean** (son el instrumento). HH1, HH2 y HH5 son la **hipótesis**: si fallan, se escriben en §10 y
**el bloque corre con esta letra**. Un humo no puede refutar ni confirmar nada (n = 1–2, semillas ya vistas).
**Ningún umbral se cambia después del humo** (regla 4).

---

## 9. Arnés — resultado: **99/99** (un proceso, T = 20 000, semillas 1–2; salida completa en el informe)

`organismo_f9.py` **`3a821884394d66c9`** · `construye_f9.py` · 11 anclas, 3 sustituciones en línea, ninguna consume el
`rng` del mundo (guardia por regex del constructor) · 475 → 540 líneas.

(A) apagada ≡ `organismo_alma2` en los 5 modos de herencia de H-1 y en 4 brazos con alma · (B) `vivo=0, n_nec=1` ≡
**TRONCO v14.1** · (C) **NADA ≡ `organismo_vivo_h1` NADA_CM, M1 ≡ M1_CM, RENACE ≡ RENACE_CM** · (D) antes de la
primera lectura del nodo, REL ≡ REC salvo el eco de configuración, y `lect_div` = 0 en los dos · (E) **deben diferir**:
REL≠REC, REL_BAR≠REL, REL_AZAR≠REL, REL_FIJO≠REL, REL_FIJO≠REC, REL_TARDE≠REL, REL_TARDE≠NADA, M1≠NADA, REC≠NADA,
`rep_acum` 1≠0 en NADA y en REL · (F) la relevancia releva (`lect_div`>0 en REL/REL_FIJO/REL_AZAR, =0 en REC; con
`nodo_lee` enorme REL_FIJO ≡ REC y REL sigue difiriendo **por el orden**) · (G) `rep_acum` acumula, no regala · (H)
contabilidad en los 8 brazos mortales × 2 niveles · (I) guardias · (J) determinismo.

**Cinco casos del arnés que fallaron en su primera versión, y por qué (declarado; ninguno era del instrumento):**
(1) (D) y (F4) comparaban también la clave `f9`, que es **eco de la configuración** (`nodo_rel` 0 contra 1), no
estado → se excluye y se añade la prueba directa `lect_div = 0`. (2) (D) usaba `T` = paso de la primera muerte **+1**,
con lo que el primer nacimiento y la primera lectura **ya habían ocurrido** → se corrige a `T` = el paso de la muerte.
(3) (G2) estaba mal escrito (una condición que no probaba lo que decía) → se reescribió como "ningún descendiente
llega antes de 500 pasos del nacimiento de su cuerpo". (4) **(F4) daba por hecho que con `nodo_lee` enorme "no hay
nada que seleccionar" y por tanto REL ≡ REC: es FALSO para la relevancia VIVA**, que lee el mismo conjunto en **otro
orden**, y para una regla delta el orden importa → la identidad se prueba ahora contra **REL_FIJO** y se añade (F6),
que exige que REL **sí** difiera. (5) La guardia `f9=1 sin h1` resultó **inalcanzable** por la cadena de guardias que
ya existía (`f9` ⇒ `alma≠None` ⇒ `muerte_real=1` ⇒ `h1=1` ⇒ `rep2=1`): se declara inalcanzable y se prueba en su lugar
que con `alma=None` la perilla se apaga sola.

---

## 10. Humo — resultado (21-sep 14:46; `datos/humo/f9_humo_20260921_144606.{log,json}`, sha del JSON `32490c65c0d0bf26`; identidad dentro del runner 3/3; 51 s las 6 corridas; UN proceso, sin `Pool`)

| brazo | s | **R₀** | r | vida med | cuerpos | **p1** | c1 | t_ok | lect_div | fundaciones | coherente |
|---|---|---|---|---|---|---|---|---|---|---|---|
| NADA | 1 | **0.182** | −188 | **125** | 231 | **0.216** | 0.986 | 21.5 | — | 188 | sí |
| REC | 1 | 0.226 | −129 | 417.5 | 168 | 0.884 | 0.974 | 39.0 | 0/37 | 129 | sí |
| **REL** | 1 | **0.408** | **−92** | **598** | 157 | **0.960** | 1.000 | 36.0 | 37/37 | 92 | sí |
| NADA | 2 | **0.159** | −190 | **119** | 227 | **0.203** | 0.992 | 30.0 | — | 190 | sí |
| REC | 2 | 0.212 | −144 | 420 | 184 | 0.778 | 0.975 | 29.0 | 0/44 | 144 | sí |
| **REL** | 2 | **0.344** | **−98** | **533** | 151 | **0.959** | 0.991 | 40.5 | 44/44 | 98 | sí |

**HH1, HH2, HH3, HH4, HH5: SÍ (5/5).**

- **El ancla es exacta, dígito a dígito.** NADA da `R₀` **0.182 / 0.159**, vida **125 / 119**, `r` **−188 / −190** y
  **188 / 190** fundaciones: **son los cuatro números del humo de H-1**
  (`PREREGISTRO_h1_muerte.md` §10: 0.182/0.159, 125/119, −188/−190, 188/190). El brazo NADA de la fase 9 **es**
  NADA_CM de H-1, no una aproximación.
- **El cuerpo nuevo conectado rechaza el veneno en su primer encuentro**: `p1` pasa de **0.21 / 0.20** a
  **0.96 / 0.96**, con `c1` **sin caer** (1.00 / 0.99 contra 0.99 / 0.99). La vida mediana pasa de 125/119 a
  **598 / 533** (4.8× / 4.5×) y las fundaciones (linaje extinguido) de 188/190 a **92 / 98**.
- **La relevancia le gana a la recencia en las dos semillas** (`R₀` 0.41 contra 0.23 y 0.34 contra 0.21; vida 598
  contra 418 y 533 contra 420), y `lect_div` es **37/37 y 44/44** en REL contra **0** en REC: la perilla no es inerte.
- **`t_ok` mide al revés, como estaba escrito en §6(ii):** NADA 21.5 / 30.0 contra REL 36.0 / 40.5. **Mi predicción
  (ii) se cumple y por eso `t_ok` no es puerta**: el cuerpo que muerde todo llega antes a su primera comida.
- **`r` sigue negativo y `R₀` sigue por debajo de 1 en los tres brazos**: con `rep_acum = 0` el linaje **no** se
  reemplaza. **H-1 y ERR-62 siguen en pie después del humo**; quien tiene que contestar eso es F9-8, y el humo no lo
  mide (las 6 corridas son `rep_acum = 0`; el único dato es del arnés a T = 20 000: los descendientes de NADA pasan de
  8 a 14).
- Ninguna cifra del humo es evidencia (n = 1–2, semillas **ya vistas**). **No se cambia ningún umbral de §5.** El
  bloque corre con esta letra en 1501–1520 y réplica 1521–1540.
