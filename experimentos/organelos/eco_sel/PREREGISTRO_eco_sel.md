# PREREGISTRO — ECO_SEL: F1 en frío con la selección natural encima. ¿Sube la capacidad del linaje? (creador, 28-sep-2026)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo.

- Frente 2 (ECO), decisión 2 de `registro/ESTADO.md`: el coordinador recomienda «F1 con la selección natural encima, sin vivero».
- Nivel 10 (JUACO-ECO). No es candidato a tronco. Carpeta `experimentos/organelos/eco_sel/`.
- Lo escribe un creador **antes del humo**; lo integra y lo corre el coordinador. §0 (shas) y §11 se completan después del arnés y del humo;
  §1–§10 son las de este texto.

## 1. De dónde sale y qué pregunta
- **F1 ARRANQUE EN FRÍO FUNCIONA ×2** (35001–35040): con la familia que pasa sólo lo que tuvo consecuencia (FAMB_RES0_ECO), el linaje se
  sostiene 1e6 pasos en ECO w90 sin vivero ni fundadores repuestos, 20/20 ×2. Su genética es MUT0: **nada varía, nada se selecciona**.
- **TERMO_EVO** (nube, 28-sep, `origin/nube/termo-evo-20260928`): un gen heredable del margen del termostato sube con herencia y no sin ella
  (18/20; larga 10/10), pero la refundación lo devuelve a la zona letal. Lección: la selección sólo acumula si el linaje no se refunda.
  En F1 frío **no hay refundación**. Ahí está la oportunidad.
- **Dato previo (descriptivo, JSON de `juaco_eco/datos/eco_v12_serie_s19701-19720`):** con vivero hasta 60 000 y 18 genes en selección,
  VIDA_T sostuvo K = 48.0 / 48.4 / 43.5 cuerpos en la 2.ª mitad (3 corridas terminadas) contra 30.2–31.6 de MUT0_T (20/20). Las otras 17
  VIDA_T pasaron de 100 000 nacimientos en un linaje (se detuvieron por ERR-60): la selección con genes de historia de vida (rep_X, dote)
  empuja a reproducirse más rápido. Por eso aquí **se separan** el margen (un gen) y el cerebro (sin historia de vida).

**Dos preguntas, dos veredictos que NO se combinan:**
- **M (la sugerida por el director):** ¿la selección sobre el **margen del termostato** como gen heredable sube la capacidad del linaje por
  encima de F1? Control: el mismo gen sin herencia.
- **C:** ¿la selección sobre los **15 genes del cerebro** (con la historia de vida fija) sube la capacidad por encima de F1? Control: los
  mismos genes sin herencia.

## 2. Mecanismo mínimo y memoria nueva
**Memoria nueva: cero. Mecanismo nuevo: cero.** Todo lo que corre ya existe y está con arnés:
- el mundo, el carro y el gemelo de F1 (`frio/motor_frio_rapido.py`, importado sin tocar);
- la genética de JUACO-ECO (`motor_eco`: 18 genes, mutación log-normal con p = 0.05 y σ = 0.15, banco de 200, 8 sombras,
  `donante` 'padre' o 'azar'), la misma de ECO v1–v2.1.

**El gen del margen.** En el carro de la familia la consigna del hambre es 1.0 (`hambre = clip(1 − E, 0, 1)`); el umbral de parto es el
gen `rep_umbral` (1.0 de fábrica). El margen es **m = 1 − rep_umbral**: de fábrica m = 0, el mismo m = 0 que en la carrera mataba a V143
(consigna = umbral, R0 0.000). En TERMO la banda que funcionó fue m ∈ [0.10, 0.40]. Aquí la consigna queda fija y lo que muta es el
umbral. **Es una analogía de margen, no el mismo mecanismo:** en este carro la boca sigue mordiendo lo bueno con p ≈ 0.84 aunque esté
lleno, y bajar el umbral también abarata el parto (el padre queda con menos reserva). Se declara así.

**Brazos** (todos: ECO w90, esc 90, 90 fundadores, quimiostato, tope 3000, carro FAMB_RES0_ECO, **t_corte = 1**, T = 1 000 000, banco 200,
8 sombras, genes cada 2 000, checkpoint cada 10 000). Sólo cambia la genética:

| brazo | genética | qué muta | de dónde sale el genoma del hijo | papel |
|---|---|---|---|---|
| **F1** | MUT0 | nada | del padre (sin mutación) | referencia: RES0_FRIO de F1 bit a bit |
| **SEL_M** | MARGEN | sólo `rep_umbral` | del padre, mutado | hipótesis M |
| **AZA_M** | MARGEN_AZAR | sólo `rep_umbral` | de una entrada AL AZAR del banco, mutada | control M: el mismo gen sin herencia |
| **SEL_C** | CEREBRO | 15 genes (todos menos dote, rep_umbral y rep_X) | del padre, mutado | hipótesis C |
| **AZA_C** | CEREBRO_AZAR | los mismos 15 | de una entrada AL AZAR del banco, mutada | control C |

- `donante = 'azar'` es el control de ECO (candidato a ERR del 23-sep ya corregido): el banco guarda el genoma NUEVO y el genoma de un
  cuerpo nunca influye en su propia copia. Es deriva sin selección. Varía igual y no se hereda.
- Sombras: 8 copias del genoma que se heredan por la misma genealogía y mutan igual, pero no actúan. Son la nula neutral dentro de la corrida.

## 3. Instrumento y anclas
- `construye_eco_sel.py` construye `nucleo_eco_sel.py` por anclas (A1–A9) desde `frio/corre_frio.py` (sha **3ba8b0f5cf1fbbfa**).
  - Copia la parte que corre (`trabajo`, `usa_gemelo`) y cambia la genética por brazo (`eco_de` = la expresión de `corre_eco.eco_cfg`).
  - Agrega `vid`: vida y causa de los nacidos en la segunda mitad.
  - Agrega `_extra_sel`: selección contra sombras en T_SEL y en T, genes de los vivos, genes fuera de los mutables.
- `corre_eco_sel.py` es el runner y la letra. `verifica()` exige el núcleo construido y los orígenes con su sha **antes de correr nada**.
- Orígenes fijados:
  - `frio/motor_frio_rapido.py` ff9d890a5cce9dec;
  - `juaco_eco/corre_eco_v12.py` 1340d268e1fd93d8, `corre_eco.py` 47d9cee4d6462116 y `motor_eco.py` bca3033878b59622;
  - `juaco_eco/carros/FAMB_RES0_ECO.py` 94ea78589bc2ce24.
- **Arnés `identidad_eco_sel.py`** (salida en `identidad_eco_sel_salida.txt`). Sin él no hay serie.
  - (K) construcción por anclas y orígenes con sha.
  - (A) `trabajo(F1)` == `corre_frio.trabajo(RES0_FRIO)` en TODAS las claves de F1.
  - (B) el gen fijo: con σ = 0, SEL_M y AZA_M == F1 bit a bit (el camino de mutación corre y no mueve nada). Controles que pueden fallar:
    - con σ = 0.15 la física difiere;
    - sólo se mueve `rep_umbral` (en C, los 3 genes de historia de vida quedan en G0);
    - AZA ≠ SEL.
  - (C) gemelo == motor Python en `trabajo()` de los 5 brazos, y con p_mut = 1.
  - (D) frío limpio, con el control de vivero que sí refunda.
  - (H) herencia exacta: en SEL todo hijo es `muta(genoma del padre)`; en AZA casi ninguno.
  - (Q) corte de luz + `--reanuda` == la corrida entera.
  - (F) nube-9.
  - (V) la letra.
  - (R) banderas.

## 4. Semillas NUEVAS
Grep del 28-sep en `*.py`, `*.md`, `*.txt` y `*.log` de `organelos` y `bundle`, y en las ramas remotas: 45xxx no se usa como semilla.
- Serie **45301–45320**; réplica **45321–45340**.
- Práctica **45391–45399**: el arnés usa 45391–45394 y el humo 45395.

## 5. Medidas
- **K, capacidad de carga del linaje:** media de los cuerpos vivos (`tam_total`, cada 1 000 pasos) en [T/2, T]; tras la extinción cuenta 0.
  - Por semilla, pareada entre brazos por semilla.
  - En F1: K = 29.9–31.7 (20/20, 35001–35020) y 30.2–31.6 en MUT0_T de ECO v1.2. Es una medida muy estable.
- **Por qué no el R0 de nacidos:** en el quimiostato un linaje que persiste tiene R0 ≈ 1 por construcción (F1: 1.0001). No puede medir
  capacidad. Se reporta y no decide.
- **Por qué no la vida sola:** la vida media cambia con la historia de vida (más partos → vidas más cortas con más cuerpos). Se reporta
  (vida media de los nacidos muertos en la 2.ª mitad) y no decide.
- **Firma de la selección contra sombras, en t = T_SEL = 100 000** (≈ 60 generaciones). Para cada semilla, el **rango** (1..9, empates a
  medias) de la media del gen en el banco real entre ella y sus 8 sombras. Bajo la nula el rango es uniforme y su media es 5.
  - M mira `rep_umbral`.
  - C mira `alpha`, `aversion` y `tau_e`: los tres que la selección movió en ECO v1, brazo CEREBRO (19101–19120): alpha + 19/20,
    aversion + 16/20, tau_e − 15/20.
  - ¿Por qué 100 000 y no 1e6? La deriva de una sombra crece como σ·√(mutaciones en la ruta). En 1e6 son ≈ 600 generaciones, unas 30
    mutaciones y DE ≈ 0.8 en log, que llenan el rango [log 0.5, log 1.45]: la prueba pierde potencia. En 100 000 la DE es ≈ 0.26.
  - Se fija antes de ver datos. La prueba de ECO (fuera de las 8 sombras) y la de T = 1e6 se reportan como descriptivas.
- Descriptivo:
  - media de los genes mutables en los vivos en T;
  - cuántas semillas de SEL_M/AZA_M dejan `rep_umbral` en la banda de TERMO [0.60, 0.90] (m ∈ [0.10, 0.40]);
  - nacimientos, vida media y fracción de muertes por veneno + sal en la 2.ª mitad;
  - persistencia y R0 de nacidos.

## 6. Criterio por la letra (`corre_eco_sel.veredicto`)
**Validez común (si falla, las dos preguntas son NO EVALUABLE):**
- serie completa: 5 brazos × 20, las mismas semillas, T = 1e6, t_corte = 1, **ningún aborto** (la guardia está en 1e9 y no puede disparar);
- bloqueados = 0;
- **V1:** F1 persiste ≥ 17/20;
- **V2:** frío limpio en los 5 brazos (0 refundados, 0 fundadores repuestos).

**Validez por pregunta:**
- **V3, la genética es la declarada:**
  - `mutables` igual al del brazo;
  - 0 valores de genes NO mutables fuera de G0 en los vivos;
  - mutación en ≥ 18/20 de SEL y de AZA, y 0 en F1.
- **Guardia de la nula:** en AZA ningún gen de la pregunta tiene rango medio ≤ 3.5 o ≥ 6.5. Si alguno lo tiene, la prueba contra sombras no
  vale y la pregunta es NO EVALUABLE.

**Puertas (por pregunta X ∈ {M, C}):**
- **P1, la selección mueve el gen:** en SEL_X, algún gen de la pregunta tiene rango medio ≤ 3.5 o ≥ 6.5. Se reporta la dirección.
- **P2, sube la capacidad sobre F1:** K(SEL_X) > K(F1), pareado, en ≥ 15/20, **y** la mediana de K(SEL_X) − K(F1) es ≥ +1.5 cuerpos.
- **P3, es la herencia y no la variación:** K(SEL_X) > K(AZA_X), pareado, en ≥ 15/20. **Es el control que puede fallar**: si el mismo gen
  sin herencia sostiene lo mismo, la capacidad no la subió la selección.

**Veredicto por pregunta:**
- **FUNCIONA**: P1 + P2 + P3.
- **HAY ALGO MODESTO: LA HERENCIA SUBE LA CAPACIDAD SOBRE F1, SIN FIRMA DEL GEN**: P2 + P3 sin P1.
- **HAY ALGO MODESTO: LA SELECCIÓN MUEVE EL GEN Y GANA A SU CONTROL, PERO NO SUPERA A F1**: P1 + P3 sin P2.
- **NO**: cualquier otro caso. En particular, P2 sin P3 («sube, pero el re-sorteo también») es NO.
- El bloque de cada pregunta se declara sólo si serie y réplica dan el mismo veredicto; si no, vale el menor.

**Nulos (regla 15):**

| puerta | nulo | umbral | P(pasa ∣ nulo) | potencia |
|---|---|---|---|---|
| P1 M (1 gen) | rango uniforme 1..9 en 20 semillas | media ≤ 3.5 o ≥ 6.5 | 0.0099 exacta (convolución) | alta si el gen está bajo todas las sombras en ≥ 1/2 de las semillas |
| P1 C (3 genes) | ídem | ídem, en algún gen | ≤ 0.030 | ídem |
| guardia AZA | ídem | ídem | falso NO EVALUABLE ≤ 0.030 | — |
| P2 | la selección no cambia K: signo p = 0.5 | ≥ 15/20 y mediana ≥ +1.5 | ≤ 0.021 | 0.80 si P(d > 0) = 0.8; 0.99 si 0.9 |
| P3 | ídem entre SEL y AZA | ≥ 15/20 | 0.021 | ídem |
| V1 | el instrumento no reproduce F1: p = 0.6 | ≥ 17/20 | 0.016 | 0.98 si p = 0.95 (F1: 20/20 ×2) |

- **Margen de P2:** la DE entre semillas de K en F1 es ≈ 0.5, así que +1.5 son unas 3 DE. No es un umbral igual a la nula.
- **Aviso honesto sobre P3 en C:** en ECO v1.2, AZAR_T (18 genes sin herencia) degeneró: 10/20 persisten con vivero, K 1–36. Si AZA_C se
  degrada, P3 C pasa con facilidad y lo que decide C es P2. Por eso P3 sola nunca da MODESTO: se exige también P1 o P2.

## 7. Predicciones firmadas (creador, antes del arnés con números de experimento y antes del humo)

| # | cantidad | rango | p |
|---|---|---|---|
| E1 | F1 persiste /20 | 19–20 | V1 0.97 |
| E2 | K de F1, mediana | [29.5, 32.5] | 0.90 |
| E3 | `rep_umbral` de los vivos en T en SEL_M, mediana sobre semillas — **baja** (m sube) | [0.52, 0.90] | 0.65 |
| E4 | P1 M (rango medio ≤ 3.5: hacia abajo) | — | 0.40 |
| E5 | K de SEL_M, mediana | [31, 48] | — |
| E6 | P2 M | — | 0.45 |
| E7 | K de AZA_M, mediana | [26, 34] | — |
| E8 | P3 M | — | 0.40 |
| E9 | SEL_M con `rep_umbral` en la banda de TERMO [0.60, 0.90] | 6–16/20 | — |
| E10 | P1 C: `alpha` sube (rango medio ≥ 6.5) | — | 0.60 |
| E11 | K de SEL_C, mediana | [28, 45] | — |
| E12 | P2 C | — | 0.45 |
| E13 | AZA_C persiste /20 · K mediana | 6–18 · [5, 30] | — |
| E14 | P3 C | — | 0.80 |
| E15 | fracción de muertes por veneno + sal en la 2.ª mitad: SEL_C < F1 (mediana) | — | 0.60 |
| E16 | veredicto M de una serie | FUNCIONA 0.15 · MODESTO 0.25 · NO 0.50 · NO EVALUABLE 0.10 | — |
| E17 | veredicto C de una serie | FUNCIONA 0.25 · MODESTO 0.40 · NO 0.25 · NO EVALUABLE 0.10 | — |
| E18 | bloque (serie + réplica iguales) | FUNCIONA ×2: M 0.10, C 0.18 | — |

**La predicción más expuesta es E3/E4.** Si la selección sube `rep_umbral` (baja el margen) o no lo mueve, la conexión con TERMO cae.
Razón de la dirección: bajar el umbral abarata el parto (la ventana de 500 pasos se cumple más a menudo), y el costo es pequeño porque
en w90 la comida conocida está a unas 20–40 celdas. En ECO v1.2 VIDA_T (18 genes) `rep_umbral` no tuvo signo claro (−0.08, +0.14, −0.14
en log), pero ahí rep_X y dote cargaban la estrategia.

## 8. Qué refuta
- **H-M:** P2 M cae con la validez intacta: la selección sobre el margen no sube la capacidad del linaje por encima de F1.
- **H-C:** P2 C cae con la validez intacta.
- **«Es la herencia»:** P3 cae (el mismo gen sin herencia sostiene lo mismo): lo que sube K es la variación, no la selección.
- **«La selección mueve el margen hacia la banda de TERMO»:** P1 M cae con la guardia en pie, o el rango medio sale ≥ 6.5 (sube el umbral).

## 9. Las cuatro trampas
1. **Canal simétrico:** SEL y AZA difieren sólo en `donante`. Tienen los mismos mutables, p, σ, banco y sombras, y la misma mutación por
   cuerpo (rng propios [seed, linaje, 16, k]). F1 difiere además en que no varía: por eso existe AZA.
2. **Acierto sin balancear:** no hay clasificación. K es un conteo pareado por semilla.
3. **Mundo que se come la comida:** el quimiostato ES esa dinámica. K sube si el mismo flujo fijo de comida sostiene más cuerpos.
   - En C la historia de vida está fija: un K mayor es mejor uso del mismo flujo.
   - En M `rep_umbral` es historia de vida: un K mayor puede venir de reproducirse con menos reserva, no de ser más hábil. Se declara y el
     vocabulario lo respeta.
4. **Sitios fijos:** los objetos aparecen en celdas libres al azar (quimiostato); la tabla de la familia es por letra, no por lugar.

## 10. Vocabulario y costo
- **Permitido:** «capacidad de carga del linaje (K = cuerpos vivos sostenidos)», «la selección mueve el gen», «margen m = 1 − rep_umbral»,
  «el mismo gen sin herencia», «sin vivero ni fundadores repuestos».
- **Prohibido:**
  - «evoluciona inteligencia», «aprende a», «especie», «población» sin la medida;
  - «TERMO emerge» (es una analogía de margen);
  - «más listo» para M.
- **Costo estimado** (F1 medido en este PC: 34–39 s por corrida a 1e6 con el gemelo):
  - los brazos con mutación suman el `objmode` del parto (9 mutaciones por nacimiento);
  - ≈ 40–120 s por corrida, 100 corridas por serie;
  - con Pool 6: **15–35 min por serie**, más si el PC está compartido. Réplica igual.
  - Cabe en el PC; la nube no hace falta. El humo mide el costo real (§11).

## 0. Instrumento (sha a 16; se completa tras el arnés, antes del humo)

| archivo | sha | qué es |
|---|---|---|
| `construye_eco_sel.py` | f2f5ed3c54d1b2c5 | constructor por anclas (A1–A9) |
| `nucleo_eco_sel.py` | 6a36e47ce61db3e1 | construido desde `frio/corre_frio.py` 3ba8b0f5cf1fbbfa (`--verifica`: IGUAL) |
| `corre_eco_sel.py` | 74aff2f668c2c97a | runner y letra (§6); `verifica()` antes de correr |
| `identidad_eco_sel.py` | 3b97f1832dba0932 | arnés; salida `identidad_eco_sel_salida.txt` (5923307f7fc00e15): **59/59** |
| `frio/motor_frio_rapido.py` | ff9d890a5cce9dec | el gemelo de F1, importado sin tocar |
| `juaco_eco/corre_eco_v12.py` · `corre_eco.py` · `motor_eco.py` · `carros/FAMB_RES0_ECO.py` | 1340d268e1fd93d8 · 47d9cee4d6462116 · bca3033878b59622 · 94ea78589bc2ce24 | orígenes (los de F1) |

§1–§10 de este archivo son las del sha **c24bceb528252e16**, escrito antes del arnés con números y antes del humo.

## 11. Arnés, humo y enmiendas (se completó DESPUÉS del arnés y del humo; §1–§10 son las del sha c24bceb528252e16)
- **Arnés, primera corrida (13:47): 57/59.** Su salida quedó guardada en `identidad_eco_sel_salida_v1_57de59.txt` (bb5eef984a04f41c).
  - Cayeron los dos casos (H) de AZA: «hijo == muta(padre)» en el 13 % (MARGEN_AZAR) y el 8 % (CEREBRO_AZAR), con un umbral de < 5 %.
  - **Candidato a ERR (el número lo pone el coordinador). Es del diseño del caso, no del instrumento.**
    - El caso contaba también a los hijos de FUNDADORES. Los 90 fundadores son clones de G0 y el banco arranca con ellos.
    - En AZA, una entrada al azar del banco coincide con el genoma de un padre fundador por identidad de clones, no por herencia.
    - Se corrigió el caso: la herencia se mide en los hijos de padres NO fundadores, cuyo genoma es único con p_mut = 1.
  - Runner, núcleo y letra sin cambios.
- **Arnés final (13:49): 59/59** en 69 s. Salida en `identidad_eco_sel_salida.txt` (5923307f7fc00e15).
  - (A) F1 == RES0_FRIO en todas las claves.
  - (B) σ = 0 == F1 en SEL_M y AZA_M, y sus tres controles fallan como deben.
  - (C) gemelo == Python en los 5 brazos y con p_mut = 1.
  - (D) frío limpio; el control con vivero refunda 340.
  - (H) SEL: 346/346 y 276/276 hijos == muta(padre). AZA: 3/203 y 0/309.
  - (Q), (F), (V) 22 casos y (R).
- **Humo (13:50):** `corre_eco_sel.py --humo`, semilla 45395, T 200 000, un proceso, 5 corridas, 23.5 s en total (4.0–5.5 s por corrida).
  - Escribió su JSON: `datos/humo/eco_sel_humo_s45395_T200000_20260928_135027.json` (fb46a6dbad22970f). La consola está en `humo_salida.txt`.
  - Los 5 brazos persisten con 0 refundados; la genética es la declarada (0 genes fuera de los mutables).
  - Veredicto de prueba: NO EVALUABLE, como debe con una semilla. **Una semilla a 200 000 no se lee, y las predicciones de §7 NO se tocan.**
- **Costo medido:**
  - ≈ 20–30 s por corrida a 1e6 (extrapolado ×5 desde 200 000; en la serie de F1 fueron 34–39 s con Pool 6).
  - Serie de 100 corridas: **≈ 10–15 min con Pool 6**, 20–30 si el PC está compartido. Réplica igual.
  - **Cabe en el PC con T = 1e6; nada tiene que ir a la nube.**
  - Opcional, sólo para la nube y descriptivo, sin letra: una larga SEL_M/AZA_M a T = 3e6 para ver si el margen sigue moviéndose.
- **Declarado:**
  - El gemelo se importa desde `frio/`: numba y Python leen o escriben su caché en `frio/__pycache__/`, que está en `.gitignore`.
  - Ningún archivo versionado fuera de `eco_sel/` se tocó.
- Sin otras enmiendas.
