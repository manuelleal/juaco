# PREREGISTRO (EXPLORATORIO) — BLOQUES: un genoma de reglas componibles sobre el bicho de fábrica (Opus M, 28-sep-2026)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo. Principio del director: que la evolución construya el órgano, no nosotros, y sólo con selección
natural. Encargo: "denle cosas que pueda usar, cosas que funcionen como Minecraft: que pueda unir, mezclar, cambiar, evolucionar".

**Esto es EXPLORATORIO** (5 semillas, T = 200 000, sin Pool). Las §1–§8 se escriben ANTES de mirar números de exploración (sólo con el
arnés corriendo). Si hay señal, §10 es el esqueleto para la nube con semillas nuevas.

## 1. Hipótesis
Con perillas fijas (15 genes) la selección llega a un techo (ING_SEL_C: K 96 → 101 a 1e6). **H-BLOQ:** si el genoma es una lista de
reglas de largo variable armadas con bloques (sentido · comparador · acción · peso) que puede leer **lo que tiene en la boca / lo que
mira** y la memoria de la última mordida, la selección arma instintos (p. ej. "no muerdas lo que tiene el píxel 4") que las 15 perillas no
pueden expresar, y la capacidad K del linaje ingenuo sube por encima de la de los 15 genes. **H-LARGO:** el genoma crece más que sin
herencia.

## 2. Mecanismo mínimo y memoria nueva
- Regla = (sentido, parámetro, comparador, umbral θ ∈ [0,1], acción, peso w ∈ [−3, 3]). Hasta NRMAX = 12 reglas.
  - Sentidos: 0 hambre, 1 sed, 2 cercanía de lo que mira, 3 píxel j del objeto en foco (lo que mira al moverse; lo que tiene en la celda
    al morder), 4 píxel j de la última letra mordida, 5 R de la última mordida.
  - Comparador: `x > θ` o `x < θ`.
  - Acciones (sesgos sumados al cerebro de fábrica): 0 boca (Vb += w), 1 patas hacia lo que mira (w > 0) / alejarse (w < 0),
    2 quedarse (las dos neuronas de marcha −= w), 3 parir (umbral de parto efectivo `ru − 0.1·Σw`, recortado a [0.5, 1.5]).
- **Genoma vacío = el bicho de fábrica bit a bit** (arnés (B)).
- Operadores (al nacer y al refundar desde el banco), todos locales, con rng PROPIO del cuerpo (etiquetas 7701/7702):
  mutar un bloque o el peso (p 0.10 por regla) · DUPLICAR una regla (Ohno, p 0.02) · BORRAR (p 0.05) · INSERTAR una regla al azar
  (p 0.02) · **HGT: copiar UNA regla entera del vecino vivo más cercano en el anillo** (p 0.01; sólo al nacer). p_del = p_dup + p_ins + p_hgt:
  sin selección el largo es un paseo sin deriva hacia arriba (con lista no vacía).
  - Por qué HGT y no recombinación: la regla es la unidad funcional (sentido+acción+peso); cruzar listas sin alinear parte reglas. El
    vecino más cercano es local (el mismo criterio que Prometeo).
- **Memoria nueva:** 2 números por cuerpo (última letra mordida y su R), que sólo leen las reglas; más el sesgo de parto del paso.
- Arranque: genoma VACÍO en los 90 fundadores (todo lo que haya al final lo armó la variación + selección).
- Banco de reglas (200): con donante 'padre' guarda la lista del PADRE en cada parto (la selección opera: sólo entra quien parió); el
  refundado toma una entrada al azar, mutada. Con 'azar' (BLOQ_AZA) guarda la lista NUEVA y todo cuerpo nuevo sale de una entrada al
  azar (el genoma nunca influye en su propia copia). Es el diseño de ECO_SEL_ING llevado a las reglas.

## 3. Qué reutilizo y qué cambia respecto de lo que ya dio NO
- Base: `eco_sel_ing/nucleo_eco_sel_ing.py` (c2189f9d22b72386) IMPORTADO sin tocar: trabajo(), K, K_nac, fund_2a, w90, vivero permanente.
- Motor: `motor_bloques.py` (39cd126e5d97c2a6), construido por 18 anclas desde `frio/motor_frio_rapido.py` (ff9d890a5cce9dec).
- Gramática (NO) y Prometeo (MODESTO; los CABLE ganaron 2 de 16): sus reglas leían estado interno (reservas, edad, ventana) y el mundo era
  el de la tabla de la familia. **Causa cambiada:** aquí el sentido puede ser la retina (píxeles del objeto) y el mundo es el de hijos
  ingenuos, donde el 96–99 % de las muertes es veneno+sal: un instinto heredable tiene dónde pagar.

## 4. Brazos (ECO w90, esc 90, 90 fundadores, quimiostato, tope 3000, FABRICA_ECO, t_corte = T, banco 200)
| brazo | genes | reglas | papel |
|---|---|---|---|
| ING_F1 | MUT0 | no | base |
| ING_SEL_C | CEREBRO (15) | no | referencia (el techo de las perillas) |
| BLOQ | MUT0 | heredables | hipótesis |
| BLOQ_AZA | MUT0 | sin herencia | control que puede fallar |
| BLOQ_C | CEREBRO (15) | heredables | ¿suman? |

## 5. Instrumento y anclas
- `construye_bloques.py` (B0–B17) → `motor_bloques.py`; `--verifica` IGUAL.
- `identidad_bloques.py` → `identidad_bloques_salida.txt`: (K) anclas y shas; (A) BQ apagado == motor_frio_rapido en todas las claves
  (3 brazos ING); (B) BQ prendido con genoma vacío y tasas 0 == fábrica (BLOQ, BLOQ_AZA == ING_F1; BLOQ_C == ING_SEL_C); (C) controles
  que deben fallar (tasas de la serie ≠; regla forzada ≠ y ACTÚA: baja la fracción de muertes por veneno+sal); (H) herencia exacta con
  tasas 0 en BLOQ, no en BLOQ_AZA; (D) determinismo.
- `corre_bloques.py --humo` (48495, T 200 000, BLOQ y BLOQ_AZA; escribe JSON) · `--explora` · `--lee`.

## 6. Medidas (por semilla, pareadas)
K = media de tam_total en [T/2, T] (copia de `corre_eco_sel_ing.kbar`); K_nac; fund_2a. Largo medio del genoma de los vivos cada 2 000
pasos y en T. Reglas "fijadas": formas (sentido(píxel) comparador → acción signo) presentes en ≥ 30 % (≥ 50 % = fijada) de los vivos en T.

## 7. Predicciones firmadas (ANTES de mirar números de exploración; 5 semillas, T 200 000)
| # | cantidad | predicción | p |
|---|---|---|---|
| M1 | K(BLOQ) > K(ING_F1) pareado | ≥ 4/5 | 0.70 |
| M2 | K_nac(BLOQ) > K_nac(BLOQ_AZA) pareado | ≥ 4/5 | 0.65 |
| M3 | **K(BLOQ) > K(ING_SEL_C) pareado** (supera el techo de los 15 genes) | ≥ 4/5 | 0.40 |
| M4 | K(BLOQ_C) > K(ING_SEL_C) pareado | ≥ 4/5 | 0.50 |
| M5 | largo medio de los vivos en T: BLOQ > BLOQ_AZA | ≥ 4/5; BLOQ en [1.5, 6], AZA en [0.3, 2] | 0.55 |
| M6 | una regla de boca negativa que separa B/D de A/C (píxel 4 `>` → boca −, o píxel 1/3 `<` → boca −) fijada (≥ 50 % de los vivos) | ≥ 3/5 semillas | 0.45 |
| M7 | fund_2a(BLOQ) < fund_2a(ING_F1) | ≥ 4/5 | 0.65 |

## 8. Control que puede fallar y qué refuta
- **BLOQ_AZA** (mismos bloques, mismos operadores, sin herencia): si BLOQ ≈ BLOQ_AZA, lo que sube no es selección de reglas.
- Refuta H-BLOQ: K(BLOQ) ≤ K(ING_SEL_C) (no supera el techo) o K_nac(BLOQ) ≤ K_nac(BLOQ_AZA).
- Refuta H-LARGO: largo(BLOQ) ≤ largo(BLOQ_AZA).
- Las cuatro trampas: (1) canal simétrico: BLOQ y BLOQ_AZA difieren sólo en el donante de reglas; mismos rng, operadores y banco.
  (2) acierto sin balancear: no hay clasificación; conteos pareados. (3) subsidio del vivero: por eso K_nac y fund_2a. (4) sitios fijos:
  los objetos y refundados en celdas al azar; **pero el significado de las letras es fijo en este mundo** (A comida, B veneno, C agua,
  D sal): un instinto "no muerdas píxel 4" vale sólo porque el mundo no cambia de reglas. Declarado: no mide aprendizaje, mide instinto.

## 9. Mini-prueba, números y errores de instrumento
(se completa después del arnés y de la exploración; §1–§8 no se tocan)

### 9a. Enmienda de las 19:29, escrita DESPUÉS de ver la exploración con vivero permanente y ANTES de correr el vivero finito
- Visto: BLOQ fija un instinto de rechazo 5/5 y baja fund_2a −66 %, pero K y K_nac quedan POR DEBAJO de ING_F1. Diagnóstico
  (`diag_mundo.py`, 48494, T 60 000, regla forzada): el instinto deja el anillo lleno de veneno y sal (B 101 → 172, D 91 → 168 de 360;
  A 36 → 10), el tope de 360 objetos se llena y se pierde el 71 % de las llegadas. En este mundo **morder veneno limpia el anillo**
  (trampa 3, "mundo que se come la comida", al revés: nadie recoge lo malo). Además el vivero permanente subsidia a quien muere rápido.
- Prueba nueva SIN subsidio (declarada antes de correrla): brazos `*_V` = los mismos con t_corte = 100 000 (sin fundadores repuestos
  después), T = 200 000, 48401–48405. Medidas: persiste en T, K en [100 000, 200 000], composición del mundo.
- Predicciones:
  | # | cantidad | predicción | p |
  |---|---|---|---|
  | V1 | ING_F1_V persiste | ≤ 1/5 | 0.80 |
  | V2 | ING_SEL_C_V persiste | ≥ 2/5 | 0.60 |
  | V3 | BLOQ_V persiste | ≥ 3/5 | 0.50 |
  | V4 | K(BLOQ_V) > K(ING_SEL_C_V) pareado | ≥ 3/5 | 0.45 |
  | V5 | BLOQ_AZA_V persiste | ≤ 1/5 | 0.65 |

### 9b. Números (EXPLORATORIO; 1 proceso por corrida, 3 procesos, T 200 000). Instrumento: construye_bloques 05bf42e0505db9a7 ·
motor_bloques ce66d09804660588 · corre_bloques 1765d9d0e7f4348e · identidad_bloques b9093495fb960fdc · diag_mundo 3410becc27e9c8d8.
Arnés 17/17 (salida en `identidad_bloques_salida.txt`, repetido al final con el runner definitivo). Humo 48495 (`humo_salida.txt`).

**Vivero permanente** (`datos/explora`, 48401–05; medianas): K · K_nac · fund_2a
- ING_F1 96.11 · 12.50 · 25 762 | ING_SEL_C 102.20 · 18.17 · 17 283 | **BLOQ 95.50 · 9.25 · 8 464** | BLOQ_AZA 94.82 · 9.02 · 23 532 | BLOQ_C 97.05 · 13.25 · 8 543
- BLOQ − ING_F1: K 0/5, K_nac 0/5, fund_2a −17 220 (5/5 menor). BLOQ − ING_SEL_C: K 0/5 (−6.8). BLOQ − BLOQ_AZA: K 4/5 (+0.8), K_nac 3/5, fund_2a 5/5 menor.
- Diagnóstico (`diag_mundo.py`, 48494, T 60 000): con el instinto el anillo se llena de veneno y sal (B 101 → 172, D 91 → 168 de 360; A 36 → 10; 71 % de
  llegadas perdidas). Con vivero permanente, K premia a quien muere rápido (dote de cada refundado) y a quien limpia el anillo mordiendo veneno.

**Vivero finito** t_corte 100 000 (sin subsidio después; `datos/vivero100k`, 48401–05, y mini-réplica `datos/vivero100k_rep`, 48406–10):
| brazo | persiste 48401–05 | K mediana | persiste 48406–10 | K mediana |
|---|---|---|---|---|
| ING_F1_V | 0/5 | 1.34 | 0/5 | 1.29 |
| ING_SEL_C_V (15 genes) | 4/5 | 8.41 | 5/5 | 10.65 |
| **BLOQ_V** | **5/5** | **37.01** | **5/5** | **36.45** |
| BLOQ_AZA_V | 1/5 | 2.13 | 0/5 | 1.87 |
| BLOQ_C_V | 5/5 | 37.01 | – | – |
| FORZ_V (mi instinto a mano, 1 copia, −3) | 5/5 | 27.47 | – | – |
| FORZ2_V (genoma evolucionado trasplantado) | 5/5 | 38.50 | – | – |
| FORZ3_V (mi instinto DUPLICADO, 2 × −3) | 5/5 | 38.66 | – | – |
- BLOQ_V > ING_SEL_C_V pareado 5/5 (+28.8) y 5/5 (+25.5); > BLOQ_AZA_V 5/5 y 5/5. Linajes reales: 1–2 por semilla, generación 24–43, K_nac ≈ K.
- Predicciones §7 (vivero permanente): M1 **REFUTADA** (0/5), M2 **REFUTADA** (3/5), M3 refutada (0/5; p 0.40), M4 **REFUTADA** (2/5), M5 **REFUTADA** (la
  deriva de BLOQ_AZA alarga más el genoma: 4.05 vs 2.74), M6 acierta (5/5), M7 acierta (5/5). §9a (vivero finito): V1–V5 aciertan las cinco.

**Órganos armados por la selección (lo que quedó fijado en los linajes que prosperan):**
1. **Instinto de rechazo por la retina** (9/10 semillas de BLOQ_V, 5/5 de BLOQ, 3/5 de BLOQ_C; 100 % de los vivos): "no muerdas lo que tiene el píxel 4"
   o "no muerdas si falta el píxel 1". Los dos separan EXACTO veneno+sal (B, D) de comida+agua (A, C). Nadie lo escribió.
2. **Duplicación como volumen (Ohno):** el rechazo aparece en ≥ 2 copias en el 85–100 % de los vivos, con peso total −4.4 a −8.4 (cada regla está recortada
   a |3|). La copia ES la función: mi instinto de una copia da K 27.5; duplicado, 38.7; el evolucionado, 37–38.5.
3. **Cautela por necesidad o memoria** (48406, más débil, K 15): "si no tienes mucha sed, muerde menos" / "si lo último que mordiste dolió, no muerdas".
   Accesorios frecuentes (30–80 % de los vivos en algunas semillas): "parir antes" tras una mordida buena o con sed.
- **¿El genoma crece?** De 0 a 2–4 reglas (hasta 6.4 en 48407) y se queda allí: crece por duplicar el órgano, no sin límite. Sin herencia deriva más largo.

**Errores de instrumento y lectura (declarados):**
- E1 (arnés): la prueba (H) de BLOQ_AZA contaba hijos de padres vacíos (16/17); corregida para contar sólo padres con reglas → 17/17.
- E2 (instrumento, antes de números): el banco de reglas arrancaba vacío; ahora arranca con las listas de los fundadores, como E9 del original.
- **E3 (candidato a ERR, el número lo pone el coordinador): con vivero permanente K no es monótono en la calidad del organismo.** El vivero subsidia a quien
  muere rápido (dote de cada refundado) y morder veneno limpia el anillo (tope de 360 objetos); un organismo que ya no se envenena baja K y K_nac. Afecta la
  lectura de cualquier genoma que evite el veneno (también el de 50 genes de Opus G).
- E4: `nucleo_eco_sel_ing.trabajo()` descarta `pista.comp_mundo` y `llegadas_perdidas`; se capturan envolviendo run_solapadas (`corre_bloques._rs`).
- E5: `--reanuda` NO sirve para las reglas: el banco de reglas y BQ_OUT viven en `_CTX` y no entran al checkpoint. Para la nube hay que agregarlos al blob.
- E6: mis horas en el canal iban ~3 min adelantadas (declarado en el canal).
- Trampa 4 declarada: el significado de las letras es fijo en este mundo; lo que se mide es un INSTINTO heredable, no aprendizaje.

## 10. SERIE CONFIRMATORIA EN EL PC (FINAL; escrita a las 19:55 del 28-sep, ANTES de la serie; la corre el coordinador después del auditor)
Pedido del coordinador (19:49): serie confirmatoria esta noche si cabe antes de las 21:50. Esta §10 reemplaza al esqueleto de nube de las 19:47 (mismas
puertas; se agregan el T medido, la validez completa y la regla MODESTO cerrada).

- **Pregunta:** sin vivero después de t_corte, ¿el genoma de reglas heredable sostiene al linaje ingenuo por encima del techo de los 15 genes?
- **Brazos** (w90, esc 90, 90 fundadores, quimiostato, tope 3000, FABRICA_ECO, **t_corte = 100 000**; reglas: tasas de §2, arranque VACÍO, banco 200):
  ING_F1_V (MUT0, sin reglas) · ING_SEL_C_V (CEREBRO 15 genes, sin reglas) · BLOQ_V (MUT0 + reglas, donante padre) · BLOQ_AZA_V (MUT0 + reglas, donante azar).
  FORZ_V/FORZ2_V/FORZ3_V NO entran (fueron referencias exploratorias).
- **T = 500 000.** Costo medido (19:50, práctica 48496, 1 proceso con otro proceso al lado y un examen con Pool 6 en el PC): BLOQ_V 63.5 s
  (persiste, K 35.25), ING_SEL_C_V 43.7 s (persiste, K 8.66); ING_F1_V y BLOQ_AZA_V se extinguen hacia t ≈ 110 000–160 000 y cuestan como a 200 000
  (21–48 s, mediana ~27 s). Proyección: ≈ 165 s por semilla × 20 / 6 ≈ 9–10 min por serie con Pool 6; × 1.5–2 por el PC compartido ≈ 14–20 min;
  **serie + réplica ≈ 30–40 min**. Cabe antes de las 21:50 si se lanza antes de ~21:00 (mejor tras las 20:30, cuando termina el otro Pool 6).
  Si no cabe: T = 300 000 con t_corte 100 000 (mismas puertas), declarado aquí como plan B; o mañana.
- **Medidas (por semilla, pareadas):** persiste en T (`persiste` del núcleo: sin extinción y con vivos al final); K = media de tam_total en [T/2, T]
  (= [250 000, 500 000]; tras la extinción cuenta 0; copia de `corre_eco_sel_ing.kbar`); frac_rechazo = fracción de los vivos en T con ≥ 1 regla de
  boca con w < 0 sobre el píxel del foco cuya condición se cumple EXACTAMENTE en B y D y no en A ni C (`corre_bloques.rechazo`; sin vivos → no cuenta).
- **Validez (si falla algo: NO EVALUABLE):** V0 serie completa: 20 semillas × 4 brazos, las mismas, T 500 000, t_corte 100 000 en todas, ningún aborto,
  bloqueados 0 · V1 la base sin vivero muere: ING_F1_V persiste ≤ 3/20 · V2 carro FABRICA_ECO en todas y reglas declaradas por brazo (BLOQ_V on/padre,
  BLOQ_AZA_V on/azar, ING sin reglas).
- **Puertas:**
  - **P1** BLOQ_V persiste ≥ 17/20.
  - **P2** K(BLOQ_V) > K(ING_SEL_C_V) pareado en ≥ 15/20 **y** mediana de la diferencia ≥ +10.
  - **P3** (control que puede fallar) K(BLOQ_V) > K(BLOQ_AZA_V) pareado en ≥ 15/20 **y** BLOQ_AZA_V persiste ≤ 5/20.
  - **P4** (firma) frac_rechazo ≥ 0.5 en ≥ 12/20 semillas de BLOQ_V.
- **Veredicto por serie (`corre_bloques.veredicto`):** FUNCIONA = P1+P2+P3+P4 · MODESTO = P3 y (P1 o P2), sin ser FUNCIONA · NO en otro caso ·
  NO EVALUABLE si falla V0, V1 o V2. **El bloque se declara sólo si serie y réplica coinciden; si no, vale el menor.**
  (Cambio respecto del esqueleto de las 19:47, hecho ANTES de datos: el esqueleto dejaba P2+P3+P4 sin P1 como NO; ahora es MODESTO.)
- **Nulos:** puertas de signo con p = 0.5, ≥ 15/20 → 0.021; P1 bajo p = 0.5 → 0.0002; P4 ≥ 12/20 bajo p = 0.5 → 0.25 (P4 es firma, no prueba sola).
- **Predicciones firmadas (antes de la serie; desde la exploración de §9b):** P1 0.85 · P2 0.80 · P3 0.85 · P4 0.75 · V1 0.95 · FUNCIONA en una serie 0.60 ·
  **FUNCIONA ×2 0.50**. K(BLOQ_V) mediana en [28, 42] (p 0.75); K(ING_SEL_C_V) mediana en [4, 15] (p 0.75). La más expuesta: P2 a 500 000 (el anillo lleno
  de veneno podría matar también a BLOQ_V; la práctica 48496 persiste con K 35.25).
- **Qué refuta:** H-BLOQ cae si P2 cae con la validez intacta (no supera el techo de los 15 genes sin subsidio); «es la herencia» cae si P3 cae;
  «es el órgano de rechazo» se debilita si P1–P3 pasan y P4 cae (otra cosa sostiene al linaje).
- **Trampas:** (1) BLOQ_V y BLOQ_AZA_V difieren sólo en el donante de reglas; (2) conteos pareados; (3) después de t_corte no hay subsidio: K es de
  NACIDOS; el anillo se llena de veneno en todos los brazos que persisten (medido en §9b), la comparación es en el mismo mundo; (4) letras de significado fijo:
  se mide un INSTINTO heredable, no aprendizaje.
- **E5 arreglado:** el banco de reglas y la telemetría viajan dentro de ES (entra al blob del checkpoint); arnés (Q): corte en 30 000 + reanuda == entera.
  `--reanuda` vale para la serie.
- **Semillas NUEVAS** (grep del 28-sep; 484xx libre salvo 48401–48410 y 48491–48496 usadas hoy): **serie 48411–48430, réplica 48431–48450**; práctica usada:
  48496 (costo a 500 000, números vistos y declarados arriba).
- **Comandos (sólo el coordinador), desde la raíz del repo:**
  - serie: `python experimentos/organelos/bloques/opusM/corre_bloques.py --serie --desde 48411 --n 20 --T 500000 --pool 6`
  - réplica: `python experimentos/organelos/bloques/opusM/corre_bloques.py --serie --desde 48431 --n 20 --T 500000 --pool 6`
  - si se corta: el mismo comando con `--reanuda`. Datos en `opusM/datos/serie_s<desde>-<fin>_T500000/` (M_*.json y VEREDICTO.json).
- **Instrumento de la serie (sha a 16):** construye_bloques 28ba92383aff5e5f · motor_bloques ff782697e54585a5 (`--verifica` IGUAL) · corre_bloques
  a090b82eae9f1ee3 · identidad_bloques 06ff008d0d53723e → `identidad_bloques_salida.txt` 08379bb785e66728: **37/37 en 212 s** (K, A, B, C, H, D, Q, L, R).
  El trabajador de la serie (`_job`) se probó en un proceso, sin Pool, en los 4 brazos a T 20 000 con la práctica 48496 (`datos/humo_job`); el Pool mismo
  no lo corrió el creador (regla).
