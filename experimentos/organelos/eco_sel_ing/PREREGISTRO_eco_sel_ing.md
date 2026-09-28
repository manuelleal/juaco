# PREREGISTRO — ECO_SEL_ING: la selección de ECO_SEL con el hijo INGENUO. ¿Sigue subiendo K? (creador, 28-sep-2026)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo. Principio del director: que la evolución construya el órgano, no nosotros.

- Frente 2 (ECO), nivel 10. No es candidato a tronco. Carpeta `experimentos/organelos/eco_sel_ing/`.
- Lo escribe un creador **antes del arnés con números de experimento y antes del humo**; lo integra y lo corre el coordinador.
  §0 y §11 se completan después; §1–§10 son las de este texto.

## 1. De dónde sale y qué pregunta
- **ECO_SEL = FUNCIONA ×2** (45301–45340): con la tabla de la familia (FAMB_RES0_ECO) y en frío, la selección sobre los 15 genes del
  cerebro sube K de ~31 a ~39.
- **eco_a_carrera = NO** (a46d53c): ese genoma, en la pista de la carrera, empeora al fundador (38.5 fundadores por linaje contra 19.5).
  Hipótesis del coordinador: ECO seleccionó cerebros que rinden **con** la tabla heredada; en la carrera el fundador empieza de cero.
- **Pregunta:** si cada cuerpo nace ingenuo (hereda los GENES, no la tabla), ¿la selección sigue subiendo K sobre la misma base sin
  selección? ¿Y el genoma que resulta sirve a un cuerpo que empieza de cero?

## 2. Qué es «la tabla de la familia» y cómo se apaga (memoria nueva: cero; mecanismo nuevo: cero)
- En `FAMB_RES0_ECO` la única memoria que pasa del padre al hijo es la **tabla**: `al_parir` da, por (necesidad, letra), la R vivida más
  reciente o, si no la vivió, la recibida. `nace` quita las R = 0 (SIN0), la instala en el nodo y la lee `NODO_LEE` veces.
  Todo lo demás (Wl, KW) sale nuevo del rng del hijo (`hereda='nada'`).
- **`diff FABRICA_ECO.py FAMB_RES0_ECO.py`** (leído el 28-sep): la única diferencia de conducta son `MODO`/`SIN0`, `al_parir` (devuelve
  la tabla en vez de `None`) y `nace` (instala la tabla). El resto es telemetría. **FABRICA_ECO es exactamente FAMB_RES0_ECO sin la
  herencia de la tabla.** En el gemelo, `LFAM = 0` salta `_tabla_padre` y `_nace_fam` y nada más; la genética (`_hijo_eco`) es la misma.
- **Por eso el carro ingenuo es FABRICA_ECO**, el mismo del brazo FAB_FRIO de F1 y de ECO v1/v1.1. No se toca ningún archivo.

## 3. ¿El linaje ingenuo persiste en frío sin vivero? NO. La base mínima que persiste (declarada antes de cualquier dato nuevo)
- **En frío:** FAB_FRIO de F1 (FABRICA_ECO, MUT0, t_corte 1) persistió **0/20** (se extingue en t ≈ 2 800 en el humo). No hay K que medir.
- **Tras un vivero finito:** en ECO v1.1 (el mismo mundo w90, FABRICA_ECO, vivero hasta 60 000), MUT0 persistió **0/20 ×2** a 1e6.
  CEREBRO persistió 7/20 y 11/20: con un vivero finito la base es 0 y P2 se volvería «SEL persiste», que ya se midió.
- **Base mínima que persiste: el VIVERO PERMANENTE** (`t_corte = T`): un linaje extinto se refunda desde el banco en todo t < T
  (`refunda = 1`, `motor_eco` E9: genoma del banco, mutado). Es el régimen de la carrera: el linaje se refunda hasta que se establece.
  - Con `donante 'padre'` el banco guarda el genoma de los PADRES (los que se reprodujeron): la selección opera.
  - Con `donante 'azar'` guarda genomas nuevos al azar (hijos y refundados): varía igual, no se hereda.
- **Datos previos (de disco, registrados, vistos al escribir esto; declarados):** JSON de `juaco_eco/datos/eco_v11_serie_s19401-19420`,
  en la ventana de vivero [30 000, 60 000]:
  - K mediana: MUT0 96.1 (95.6–97.2) · CEREBRO 103.6 (101.4–105.1) · AZAR (18 genes) 92.4 · CEREBRO > MUT0 20/20 y > AZAR 20/20;
  - refundaciones hasta 60 000: MUT0 15 331 · CEREBRO 12 192 · AZAR 15 551; CEREBRO < MUT0 20/20 y < AZAR 20/20.
  - **Honestidad:** esto ya dice que la selección con hijo ingenuo sube K en una ventana corta de vivero. Lo nuevo aquí es:
    (i) el horizonte (1e6, ≈ 17× más selección) y si sigue acumulando; (ii) el control de 15 genes sin herencia (el de v1.1 tenía 18);
    (iii) K_nac y el establecimiento (fund_2a), la palanca del muro; (iv) el genoma que sale, para llevarlo a la carrera.

## 4. Brazos (todos: ECO w90, esc 90, 90 fundadores, quimiostato, tope 3000, carro FABRICA_ECO, t_corte = T, banco 200, 8 sombras,
genes cada 2 000, checkpoint cada 10 000). Sólo cambia la genética, la MISMA de ECO_SEL:

| brazo | genética | qué muta | genoma del hijo (y del refundado) | papel |
|---|---|---|---|---|
| **ING_F1** | MUT0 | nada | G0 | base ingenua sin selección |
| **ING_SEL_C** | CEREBRO | 15 genes (todos menos dote, rep_umbral, rep_X) | del padre, mutado (refundado: del banco de padres) | hipótesis |
| **ING_AZA_C** | CEREBRO_AZAR | los mismos 15 | de una entrada AL AZAR del banco de genomas nuevos, mutada | control: sin herencia |

- ING_SEL_M / ING_AZA_M: **no entran** (tiempo; sin su AZA no hay P3). Quedan para después si C da algo.

## 5. Instrumento y anclas
- `construye_eco_sel_ing.py` construye `nucleo_eco_sel_ing.py` por anclas (B1–B8) desde `eco_sel/nucleo_eco_sel.py` (sha
  **6a36e47ce61db3e1**). Los cinco brazos de ECO_SEL quedan sin tocar (para el arnés). Se agregan:
  - los tres brazos ING (carro FABRICA_ECO, t_corte None = T);
  - `k2`: (tn, tm, fund) de todo cuerpo vivo en algún momento de [T/2, T];
  - `_extra_ing`: **K_nac** (nacidos) y **K_fund** (fundadores) con el mismo muestreo que `tam_total`; **fund_2a** (fundadores
    repuestos con tn ≥ T/2). K_nac + K_fund == K (arnés).
- `corre_eco_sel_ing.py`: runner y letra. `verifica()` exige el núcleo construido y los orígenes con su sha antes de correr.
  `kbar` y `rango` son copia textual de `eco_sel/corre_eco_sel.py` (el arnés las compara en entradas).
- Orígenes fijados: `eco_sel/nucleo_eco_sel.py` 6a36e47ce61db3e1 · `eco_sel/corre_eco_sel.py` 74aff2f668c2c97a ·
  `frio/corre_frio.py` 3ba8b0f5cf1fbbfa · `frio/motor_frio_rapido.py` ff9d890a5cce9dec · `juaco_eco/corre_eco_v12.py` 1340d268e1fd93d8 ·
  `corre_eco.py` 47d9cee4d6462116 · `motor_eco.py` bca3033878b59622 · `carros/FAMB_RES0_ECO.py` 94ea78589bc2ce24 ·
  `carros/FABRICA_ECO.py` f1163009cb5193a2.
- **Arnés `identidad_eco_sel_ing.py`** (salida `identidad_eco_sel_ing_salida.txt`). Sin él no hay serie.
  - (K) construcción por anclas y orígenes con sha.
  - (A) los brazos de ECO_SEL (F1, SEL_C) en el núcleo ING == `nucleo_eco_sel.trabajo` en TODAS sus claves (sólo se agregan las de
    `_extra_ing`); ING_F1 con t_corte 1 == `corre_frio.trabajo(FAB_FRIO)` en todas las claves de F1 (la base ingenua es la de F1).
  - (I) **ingenuo:** ING_F1 difiere de F1 (el control que puede fallar: si la tabla no hiciera nada, serían iguales).
  - (B) **σ = 0:** ING_SEL_C e ING_AZA_C == ING_F1 bit a bit (con vivero permanente) salvo claves de configuración.
    Controles: con σ = 0.15 la física difiere; AZA ≠ SEL.
  - (H) herencia exacta con p_mut = 1 (FABRICA_ECO, vivero permanente): en SEL todo hijo de padre no fundador == muta(padre);
    en AZA < 5 % (caso H de ERR-149: sin contar hijos de fundadores).
  - (V) vivero permanente: refunda en todo el horizonte (fund_2a > 0); K_nac + K_fund == K exacto.
  - (C) gemelo == motor Python en los tres brazos ING (T corto).
  - (D) determinismo: dos corridas iguales == bit a bit.
  - (Q) corte de luz + `--reanuda` == la corrida entera (k2 en el checkpoint).
  - (L) la letra en entradas sintéticas; (R) banderas.

## 6. Criterio por la letra (`corre_eco_sel_ing.veredicto`)
**Medidas** (por semilla, pareadas por semilla):
- **K** = media de `tam_total` en [T/2, T] (la de ECO_SEL, misma función).
- **K_nac** = lo mismo contando sólo cuerpos NACIDOS. Existe por la trampa 3: el vivero permanente inyecta la dote de cada fundador
  repuesto; K solo podría subir comprando fundadores.
- **fund_2a** = fundadores repuestos con tn ≥ T/2 (lo que cuesta establecerse; la palanca del muro).

**Validez (si falla, todo es NO EVALUABLE):** serie completa (3 × 20, mismas semillas, T declarada, t_corte = T, ningún aborto);
bloqueados = 0; **V1** ING_F1 persiste ≥ 17/20 (con vivero permanente debe ser 20/20); **V2** carro FABRICA_ECO en los tres brazos;
**V3** genética declarada (mutables del brazo, 0 genes fuera de los mutables movidos, mutación en ≥ 18/20 de SEL y AZA, 0 en ING_F1).
**Guardia de la nula:** en ING_AZA_C ningún gen de {alpha, aversion, tau_e} con rango medio ≤ 3.5 o ≥ 6.5.

**Puertas (las de ECO_SEL, pregunta C; + K_nac):**
- **P1** en ING_SEL_C algún gen de {alpha, aversion, tau_e} con rango medio contra sus 8 sombras, en t = 100 000, ≤ 3.5 o ≥ 6.5.
- **P2** K(SEL) > K(F1) pareado en ≥ 15/20 **y** mediana de la diferencia ≥ +1.5 **y** K_nac(SEL) > K_nac(F1) en ≥ 15/20.
- **P3** K(SEL) > K(AZA) en ≥ 15/20 **y** K_nac(SEL) > K_nac(AZA) en ≥ 15/20. Es el control que puede fallar.
- **P4 (establecimiento, veredicto aparte E):** fund_2a(SEL) < fund_2a(F1) en ≥ 15/20 **y** fund_2a(SEL) < fund_2a(AZA) en ≥ 15/20.

**Veredicto C:** FUNCIONA = P1 + P2 + P3 · MODESTO (sin firma) = P2 + P3 · MODESTO (no supera la base) = P1 + P3 · NO en otro caso.
**Veredicto E:** FUNCIONA = P4 completo · NO en otro caso. El bloque se declara sólo si serie y réplica coinciden; si no, vale el menor.

**Nulos (regla 15):** P1 con 3 genes ≤ 0.030 (convolución exacta del rango uniforme 1..9 en 20 semillas, como ECO_SEL);
P2, P3 y cada mitad de P4: signo con p = 0.5, ≥ 15/20 → 0.021 (con dos condiciones a la vez, ≤ 0.021); V1 bajo p = 0.6: 0.016.
Potencia: 0.80 si P(d > 0) = 0.8; 0.99 si 0.9 (en v1.1 fue 20/20 en la ventana corta).

## 7. Predicciones firmadas (antes del arnés con números y del humo)

| # | cantidad | rango | p |
|---|---|---|---|
| I1 | ING_F1 persiste /20 | 20 | 0.98 |
| I2 | K de ING_F1, mediana | [93, 100] | 0.80 |
| I3 | K de ING_SEL_C, mediana | [100, 130] | 0.75 |
| I4 | K de ING_AZA_C, mediana | [86, 99] | 0.75 |
| I5 | **K(ING_SEL_C) mediana > 103.6** (la de v1.1 en [30k, 60k]: la selección sigue acumulando con el horizonte) | — | 0.60 |
| I6 | fund_2a de ING_F1, mediana (≈ 0.25 por paso) | [110 000, 140 000] | 0.70 |
| I7 | fund_2a de ING_SEL_C, mediana | [30 000, 110 000] | 0.70 |
| I8 | P1 (alpha sube: rango medio ≥ 6.5) | — | 0.80 |
| I9 | P2 | — | 0.80 |
| I10 | P3 | — | 0.80 |
| I11 | P4 (E) | — | 0.80 |
| I12 | veredicto C de una serie | FUNCIONA 0.65 · MODESTO 0.12 · NO 0.13 · NO EVALUABLE 0.10 | — |
| I13 | bloque C FUNCIONA ×2 | — | 0.50 |
| I14 | alpha de los vivos en T en ING_SEL_C > en ING_AZA_C (mediana) | — | 0.80 |
| I15 | K_nac de ING_F1, mediana | [3, 30] | 0.60 |

**La más expuesta es I5** (que la selección siga acumulando más allá de la ventana de v1.1). Si cae, la selección con hijo ingenuo
satura pronto. **Lo que NO predice este experimento:** que el genoma de ING_SEL_C mejore al fundador de la carrera; eso lo mide un
eco_a_carrera con este genoma (siguiente paso si C y E dan FUNCIONA).

## 8. Qué refuta
- **H-ING (la selección sube K con el hijo ingenuo):** P2 cae con la validez intacta.
- **«Es la herencia»:** P3 cae (el mismo gen sin herencia sostiene lo mismo).
- **«Es comprar fundadores»:** P2/P3 pasan en K y caen en K_nac (se ve en la línea de la letra) → la letra da NO.
- **«La selección abarata el establecimiento»:** P4 cae.
- **Hipótesis del coordinador (ECO_SEL eligió cerebros para la tabla):** es CONSISTENTE con ECO_SEL_ING = FUNCIONA sólo si además el
  genoma de ING_SEL_C difiere del de SEL_C de ECO_SEL (descriptivo: medias de los genes en los vivos en T, lado a lado) y mejora al
  fundador de la carrera (experimento siguiente). Aquí no se decide.

## 9. Las cuatro trampas
1. **Canal simétrico:** SEL y AZA difieren sólo en `donante`; mismos mutables, p, σ, banco, sombras, carro, vivero y rng.
   ING_F1 difiere además en que no varía (por eso existe AZA).
2. **Acierto sin balancear:** no hay clasificación; K, K_nac y fund_2a son conteos pareados por semilla.
3. **Mundo que se come la comida / subsidio:** el quimiostato fija el flujo de comida, pero el vivero permanente inyecta la dote de
   cada fundador repuesto. Por eso P2 y P3 exigen también K_nac, y P4 mira los fundadores: si SEL gana K con MENOS fundadores, no es
   subsidio.
4. **Sitios fijos:** los objetos y los refundados aparecen en celdas al azar (quimiostato; posición del rng de reaparición del linaje).

## 10. Vocabulario, costo y T
- **Permitido:** «capacidad de carga del linaje ingenuo», «la selección mueve el gen», «el mismo gen sin herencia», «fundadores repuestos».
- **Prohibido:** «evoluciona inteligencia», «aprende a», «especie», «población» sin la medida; «transfiere a la carrera» (no se mide aquí).
- **Costo:** con vivero permanente hay ≥ 90 cuerpos siempre (≈ 3× F1) y ≈ 0.25 refundaciones por paso (cada una con `objmode`).
  El humo mide el costo real.
- **Regla de T (declarada antes del humo):** proyección lineal del humo (suma de los 3 brazos a 200 000 × 5 × 20 / 6) × 1.5 de margen
  (PC compartido, K que crece):
  - si ≤ 45 min por serie → **T = 1 000 000**;
  - si no, **T = 500 000** (mismas puertas; T_SEL = 100 000 igual; K en [250 000, 500 000]);
  - si tampoco cabe, no se corre hoy y se dice.
- Semillas NUEVAS (grep del 28-sep en `*.py`, `*.md`, `*.txt`, `*.log` de organelos y bundle y en las ramas remotas; 461xx sólo
  aparece como número de tabla en `boca_buena/tabla_bb.txt`, no como semilla): serie **46101–46120**, réplica **46121–46140**,
  práctica **46191–46199** (arnés 46191–46194, humo 46195).

## 0. Instrumento (sha a 16; se completa tras el arnés, antes del humo)

| archivo | sha | qué es |
|---|---|---|
| `construye_eco_sel_ing.py` | 8c74739584d602a0 | constructor por anclas (B1–B8) |
| `nucleo_eco_sel_ing.py` | c2189f9d22b72386 | construido desde `eco_sel/nucleo_eco_sel.py` 6a36e47ce61db3e1 (`--verifica`: IGUAL) |
| `corre_eco_sel_ing.py` | cc7e8c0377f4ed88 | runner y letra (§6); `verifica()` antes de correr |
| `identidad_eco_sel_ing.py` | e50ab046bf876049 | arnés; salida `identidad_eco_sel_ing_salida.txt` (1058a2eb19fa47d0): **54/54** en 114 s |

§1–§10 de este archivo son las del sha **b3ee578f2308ceef**, escrito antes del arnés con números y antes del humo.

## 11. Arnés, humo y enmiendas (se completó DESPUÉS del arnés y del humo; §1–§10 son las del sha b3ee578f2308ceef)
- **Arnés, primera corrida (17:08): 46/52.** Dos fallos, los dos del ARNÉS (runner, núcleo y letra sin cambios):
  - (V) K_nac + K_fund == K con tolerancia 1e-9, pero `_extra_ing` redondea a 6 decimales (14.454545 + 83.0 = 97.454545 en pantalla).
    Se pasó a 1.5e-6: un cuerpo de más o de menos en una sola muestra mueve la suma ≥ 1/501. Error mío del arnés.
  - (B) **Candidato a ERR (el número lo pone el coordinador): σ = 0 NO apaga la mutación del cerebro.** `motor_eco.muta` fuerza ±1 en
    los genes ENTEROS (NK, memoria_rechazo; rep_X no muta aquí) cuando la mutación dispara, aunque σ = 0 (`round(h·e⁰) == h → h ± 1`).
    ING_SEL_C e ING_AZA_C con σ = 0 difieren de ING_F1 por eso. En ECO_SEL el caso (B) usó σ = 0 sólo con rep_umbral (real): allí
    vale y no hay error retroactivo. Aquí la perilla apagada es **p_mut = 0** (muta consume siempre 2·NG números: el rng no se corre) y
    σ = 0 queda como caso que documenta la propiedad (sólo se mueven NK y memoria_rechazo).
  - Segunda corrida: 52/54; el caso p_mut = 0 exigía `mutables` = los 15, pero el motor informa `mutables = []` con p_mut 0 (el
    arnés, no el instrumento). Se cambió a p_mut 0, n_mut 0 y el donante del brazo.
- **Arnés final (17:15): 54/54** en 114 s. Salida `identidad_eco_sel_ing_salida.txt` (1058a2eb19fa47d0). Lo que dice:
  - (A) núcleo ING con F1 y SEL_C == `nucleo_eco_sel` en todas sus claves (sólo se agregan K_nac, K_fund, fund_2a, n_k2);
    ING_F1 en frío == `corre_frio` FAB_FRIO en todas las claves (se extingue en t 5 649).
  - (I) ING_F1 ≠ F1. (V) vivero permanente refunda en la 2.ª mitad; K_nac + K_fund == K en 4 regímenes.
  - (B) p_mut 0 == ING_F1 bit a bit (SEL y AZA). (H) SEL 201/201 hijos == muta(padre), con 4 255 refundados; AZA 0/66.
  - (C) gemelo == Python en los 3 brazos ING. (D) determinismo. (Q) corte + reanuda. (L) 23 casos. (R) banderas.
- **Humo (17:17):** `corre_eco_sel_ing.py --humo`, semilla 46195, T 200 000, un proceso, 3 corridas, 64.7 s (20.5–22.5 s por corrida).
  - JSON: `datos/humo/eco_sel_ing_humo_s46195_T200000_20260928_171716.json` (f443af819ec1ecc9). Consola: `humo_salida.txt` (e3b8c84b89ce41b9).
  - Los tres brazos: carro FABRICA_ECO, t_corte = T, persisten, 0 bloqueados, 0 genes fuera de los mutables.
  - Veredicto de prueba: NO EVALUABLE, como debe con una semilla. **Una semilla a 200 000 no se lee; §7 NO se toca.**
- **Regla de T (§10) aplicada:** proyección lineal 17.9 min por serie con Pool 6; × 1.5 = 26.9 min ≤ 45 → **T = 1 000 000**.
- **Comandos (sólo el coordinador):**
  - serie: `python experimentos/organelos/eco_sel_ing/corre_eco_sel_ing.py --serie --desde 46101 --n 20 --pool 6 --T 1000000`
  - réplica: `python experimentos/organelos/eco_sel_ing/corre_eco_sel_ing.py --serie --desde 46121 --n 20 --pool 6 --T 1000000`
  - tiempo: ≈ 18 min cada una con el PC libre; 25–30 min si está compartido. Serie + réplica ≈ 40–60 min.
- **Declarado:** el gemelo se importa desde `frio/` (su caché en `frio/__pycache__/`, en `.gitignore`); el arnés importa
  `eco_sel/nucleo_eco_sel.py` y `eco_sel/corre_eco_sel.py` sin tocarlos (su caché en `eco_sel/__pycache__/`). Ningún archivo
  versionado fuera de `eco_sel_ing/` se tocó.
