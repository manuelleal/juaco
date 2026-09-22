# PREREGISTRO — FASE 10: el mundo donde un linaje mortal sólo se sostiene si transmite, y lo transmitido tiene que crecer

**Brazo F1 (Fable 5.1 + memoria del exo + aprendices Haiku), 21-sep-2026, 20:20 (§1–§9 escritos antes de leer el humo; §10 y §11 pegados después).**
**Misión:** llegar a la AGI por este camino — organismo mínimo, reglas locales, sin retropropagación, cada peldaño preregistrado, medido con controles y replicado. El método manda sobre el cómo.
**Encargo:** `equipos/fase10/ENCARGO_mundo_fase10_20260921.md` §2–§8. **Repo de JUACO:** sólo lectura (`C:\Users\User\Documents\PROYECTOS\JUACO\bundle`). **Entregables:** esta carpeta.
**Carpeta destino propuesta en JUACO (la crea el coordinador):** `experimentos/nivel10_mundo_acumula/`.

## 0. El hecho
El mundo actual del tronco (16 patrones, 6 píxeles, comida que reaparece donde estaba, visión global) no exige acumular ni saber dónde: con muerte real ningún modo de herencia sostiene el linaje (H-1 ×2, R₀ 0.14–0.17) y **ni el nodo ORÁCULO con la tabla verdadera cruza R₀ 0.90** (0.508 / 0.557, `REGISTRO_etapas_1_2.md:6003-6018, 6078-6087`). El recién nacido ya no muere de veneno: muere de hambre y sed. El muro es el mundo. Este preregistro **no propone un órgano**: propone el mundo y mide si el organismo del tronco, con el nodo de la fase 9 y el mapa de nivel 6 tal como están, lo cruza.

## 1. Hipótesis
**H10.** En un mundo donde (a) la comida se agota y se abre en otra parte, (b) la visión es limitada (saber DÓNDE cuenta), (c) los estímulos son familias × variantes con más píxeles (el alias cuesta vidas) y (d) las valencias viran sin aviso a un ritmo que una vida no alcanza a seguir, **un linaje que transmite QUÉ (patrón, R, necesidad) y DÓNDE (sitio) por el nodo de relevancia se sostiene (R₀ ≥ 1) y la generación 5 explota combinaciones que la 1 no explotaba; sin nodo, con nodo barajado, con sólo QUÉ (ORÁCULO sin mapa) o con sólo DÓNDE (mapa sin tabla) no.**
Mecanismo declarado: **cero memoria nueva en el organismo**. En el canal del linaje, **un entero más por mensaje: el sitio**. El recién nacido conectado (i) lee el nodo por relevancia viva exactamente como en la fase 9 (vía lenta) y (ii) escribe el sitio de cada mensaje leído en la tabla M del mapa de nivel 6 (`_Mpat[sitio]=patrón`), la misma tabla que él llenará al ver. Nada más.

## 2. El mundo (`mundo10=1`), con los números del §2.1 del encargo
| req. | diseño | número verificable | medida en el crudo |
|---|---|---|---|
| 1 recursos que se agotan y se mueven | `nsit10=6` sitios abiertos a la vez; cada sitio tiene `stock10=25` bocados; un bocado lo esconde `regen10=50` pasos (mundo_mapa `_pend`); al agotarse se **cierra y se abre otro en una posición sorteada por el rng del mundo**; el "olvido" del tronco (0.003/paso) traslada el sitio | comida por sitio fijo → 0 en ≤ T/4: vida mediana de un sitio hasta agotarse ≤ 25 000 | `sitios_cerrados[t_cierre−t_apertura]`, `agotados` |
| 2 saber dónde vale tanto como saber qué | visión `r_vis=8` en un anillo `L=40`: sin objeto a la vista la retina está vacía y sólo el mapa (`usa_M`, sesgo por dirección con `valor()` de la necesidad activa) o el azar mueven | R₀(ORÁCULO_SIN_MAPA) < 1 y R₀(MAPA_SIN_TABLA) < 1 y R₀(MAPA) ≥ 1 | brazos §4 |
| 3 estímulos compuestos | `nfam10=4` familias × `nvar10=2` variantes sobre `npx=9` píxeles: núcleo de peso 3 en los 6 primeros (como A–D), la variante añade **un** píxel de sufijo (6+f mod 3); 8 tipos; `flip10=1`: una variante de familia buena y una de familia mala tienen la valencia **opuesta de su eje** ("sal rosa" no es sal) | sin desambiguar códigos el alias existe: fracción de cuerpos que mueren con ≥ 1 par de tipos con el **mismo código exacto** ≥ 0.5 (se reporta también `des_splits`, las divisiones B-5 por R = 0) | `f10.alias`, `des_splits` |
| 4 cambios no avisados | cada `cambio10=12 500` pasos **un tipo bueno y un tipo malo** viran a la valencia opuesta de su eje (rng del mundo; el balance 4/4 se conserva): 7 cambios × 2 tipos = 14 viradas en T = 100 000 (t = 12 500 … 87 500) | un cuerpo (vida mediana ≈ 100) cubre < 50 % de las combinaciones útiles; el linaje a la 5.ª generación > 80 % | `f10.cuerpos[cob, lin]` |
| 5 más de un cuerpo | **opción declarada, no construida ni medida**: un cuerpo a la vez (la palabra "población" no se usa) | — | — |
| 6 coste de vida (ancla) | mismo CUERPO que H-1 y la fase 9 campo a campo (`corre_f9.CUERPO`: costo 0.001, costo_a 0.001, dote 0.6, rep_X 500, rep_umbral 1.0, rep_cuello 2, estims → sorteados) | R₀(NADA) ∈ [0.1, 0.3]; R₀(INMORTAL) ∈ [0.8, 1.3] | M10-0 |

Geometría, patrones, valencias y cambios salen de un rng **propio del mundo** (`880000+1000000*seed`, como `mundo_muralla` 1000003·seed+7): dos semillas son dos mundos y el rng del organismo no se toca (E-15, ERR-36, trampa 4). El barajado de sitios usa `890000+1000000*seed` (ERR-60).

**Calibración del ancla (sondas de UN proceso, T = 20 000–40 000, semillas 1–4, hechas ANTES del humo y declaradas aquí; ver REGISTRO.md 20:10–20:45).** Sin `regen` el cuerpo se quedaba comiendo lo que no le faltaba y moría de sed (RENACE 0.02–0.3): trampa de sitio, arreglada con el `regen` de mundo_mapa. Con variantes de valencia sorteada al 50 % salían 5/8 tipos malos y RENACE caía a 0.1–0.5: arreglado con flips balanceados. Con `cambio10=5 000` el mundo entero viraba en 20 000 pasos (RENACE 0.3–0.5); con 12 500, RENACE 0.90 [0.36–5.6] y NADA 0.30 [0.04–0.59] (4 semillas, T = 40 000). **Se fija cambio10 = 12 500 y no se vuelve a tocar.** La varianza entre semillas es grande (una semilla da RENACE 5–7): el ancla se juzga por mediana de 20.

## 3. El instrumento y las anclas (`construye_mundo_fase10.py` → `mundo_fase10.py`, sha impreso por el constructor)
| origen (sólo se leyó) | sha | qué se copió |
|---|---|---|
| `experimentos/nivel09_cuerpo_nuevo/organismo_f9.py` | `3a821884394d66c9` | **todo**: mundo vivo + reproducción + muerte real + nodo por relevancia (cadena alma2 `4fd616aeaf535e61` ← … ← v14.1 `feefc88b1fd8d434`) |
| `organismo/organismo_v142.py` | `17528d767fcebaf6` | B-5 `desambiguar` (l. 162–166, condición literal); la forma matricial `Wp[_nm,j]` de `creacion_B/organismo_vivo_codigo.py` `839fa71f9c84cb26` l. 215–219 |
| `experimentos/nivel6_mapa/mundo_mapa.py` | `207d6a1954336b18` | `r_vis` en `see()`, retina vacía, `_Mpat/_Mset`, `_sesgo_M`, `escribe_M`, `_pend/regen` (l. 36, 45, 57–60, 67, 76, 78–82, 88, 95, 104) |
| `experimentos/nivel06_rodeo_obligado/mundo_muralla.py` | `6e515713c86d8bf4` | el patrón "geometría por semilla con rng independiente" (l. 82–84) y la perilla `placebo` (k sorteos descartados) |
| `experimentos/nivel09_cuerpo_nuevo_b2/organismo_f9c.py` | `9dd1fb91ecec35ae` | el NODO ORÁCULO (l. 483–486), adaptado a `tipos` y sin sitio |
Tripwire: el constructor aborta si un sha no cuadra o si un ancla aparece ≠ 1 vez; comprueba con regex que ninguna línea nueva consume el rng del organismo salvo `placebo`. **El organismo no se modifica a mano**: todas las perillas nuevas son del mundo, del nodo o del mapa; con todas apagadas es `organismo_f9` bit a bit y con `vivo=0, n_nec=1, desambiguar=1` es el tronco v14.2 bit a bit (arnés §10).

## 4. Brazos, semillas y puertas (la letra; `corre_mundo_fase10.UMBRALES`)
**Brazos** (mismo CUERPO; T = 100 000; 20 semillas **2401–2420**, réplica **2421–2440**; grep del 21-sep en `experimentos/`, `registro/`, `datos/`: ninguna 24xx usada): INMORTAL · NADA · PLACEBO · SIN_HERENCIA · REL · **MAPA (candidato)** · NODO_BARAJADO · SITIO_BARAJADO · ORÁCULO_SIN_MAPA · MAPA_SIN_TABLA · MUNDO_FIJO · NADA_FIJO (definiciones en la cabecera del runner). 12 × 20 = 240 corridas por serie.
**R₀** = descendientes / (muertes + 1) (H-1 §3, la de la fase 9). **Cobertura de un cuerpo** = |{(tipo, necesidad) con R > 0 mordidos por ese cuerpo}| / |{(tipo, necesidad) con consecuencia positiva AHORA}|. **Generación** = partos desde el fundador (fundador = 1); se reinicia con cada fundación.

| puerta | letra (PASA si) | nulo | margen | n que deja pasar al placebo ≥ 0.95 | placebo |
|---|---|---|---|---|---|
| **M10-0 ancla (bloqueante)** | mediana R₀(NADA) ∈ [0.10, 0.30] y R₀(INMORTAL) ∈ [0.80, 1.30]; vida mediana de un sitio ≤ T/4; agotados ≥ 1; alias ≥ 0.5 | — (es el ancla del mundo; si cae, el mundo no es el que se calibró: se para y se abre ERR) | los rangos del §2.1.6 | — | — |
| **M10-1 sostén** | k(MAPA: R₀ ≥ 1.0 y fundadores ≤ 2) ≥ 15/20; mediana R₀(NADA) < 0.5; mediana R₀(NODO_BARAJADO) < 0.5; k(PLACEBO) < 15 | bajo H0 MAPA ≡ NADA: R₀ ≈ 0.3, P(R₀ ≥ 1 por semilla) ≈ 0.10 (3/16 en las sondas) | 1.0 − 0.3 = 0.7 | P(k ≥ 15 | p = 0.10, n = 20) < 10⁻¹⁰: el placebo pasa (no cruza) con prob. ≈ 1 | PLACEBO corre entre los brazos y se le aplica la misma k |
| **M10-2 acumulación** | mediana cob(gen ≥ 5) / mediana cob(gen 1) en MAPA ≥ 2.0 y A₁₂(por semilla) ≥ 0.85; NODO_BARAJADO ≤ 1.2 y PLACEBO ≤ 1.2 **si tienen ≥ 10 cuerpos de gen ≥ 5** (si no, "NO EVALUABLE", E-14, y se declara) | razón = 1.0 (la generación no cambia nada) | 2.0 − 1.0 = 1.0 en la razón; A₁₂ 0.85 vs 0.50 | con 20 semillas, P(A₁₂ ≥ 0.85 | H0) ≈ 0.001 (Mann-Whitney, n = 20/20) | ídem |
| **M10-3 no es el mundo blando** | MUNDO_FIJO razón gen5/gen1 ≤ 1.2 | 1.0 | 0.2 | si MUNDO_FIJO no llega a 10 cuerpos de gen ≥ 5 → n/a declarado | — |
| **M10-4 no regresión** | arnés I2 (12 escenarios × 2) + I3 (T = 120 000) + I4 (mapa inerte con visión ilimitada) IDÉNTICOS → G1 ≥ 0.80 / G2 ≥ 0.85 heredados **por identidad** del tronco v14.2 | — | — | — | comando para rehacerlos: `python organismo/bateria_generaliza_v142.py organismo_v142 20 --desde 101 --log` (Pool, coordinador) |
| **M10-5 representación (se reporta)** | celdas, `des_splits`, selectividad de celdas por tipo, por brazo | — | — | — | — |
| **COSTE** | muertes(MAPA)/muertes(NADA) ≤ 1.25 y celdas ≤ 1.25 en el mundo 10; en el mundo del tronco el coste es 0 por identidad | 1.0 | 0.25 | — | — |
| **SEG** | contabilidad H1-8 en todas; `frac_div`(MAPA) ≥ 0.5 y `sitios_leidos` > 0 (ERR-38); exposiciones por brazo ≥ 0.5× NADA (trampa 3); mínimo de cambios por tipo (E-10) se reporta | — | — | — | — |

Ninguna puerta usa `A₁₂ ≥ 0.50` pareado. Hasta el criterio v4, si el coordinador quiere juzgar con v2 y v3 lado a lado, las medianas y los A₁₂ están en el crudo.

## 5. Predicciones firmadas (rango + probabilidad; escritas ANTES del humo, con las sondas del §2 a la vista)
| puerta | predicción | probabilidad que declaro |
|---|---|---|
| M10-0 | R₀(NADA) mediana **[0.15, 0.35]**; R₀(INMORTAL) **[0.6, 1.4]** (las sondas dieron 0.30 y 0.90 con 4 semillas y T = 40 000; a T = 100 000 espero menos). | pasa entera **45 %** (la cola de INMORTAL es ancha: 0.36 y 5.6 en las sondas) |
| M10-1 | R₀(MAPA) mediana **[0.25, 0.60]**; k(R₀ ≥ 1) **[1, 6]** de 20. **Predigo que CAE**: el mapa de nivel 6 con visión 8 en anillo 40 no compensa 16 viradas por vida de linaje; el recién nacido sigue muriendo de sed antes de leer el sitio útil. NADA < 0.5 y NODO_BARAJADO < 0.5 sí se cumplen (95 %). | pasa **10 %** |
| M10-2 | razón gen5/gen1 en MAPA **[0.8, 1.6]**; muy pocos cuerpos de generación 5 (n **[5, 60]** en 20 semillas). **Predigo que CAE o queda NO EVALUABLE**: la cobertura de un cuerpo está dominada por ceros (la mayoría muere sin morder nada bueno). | pasa **10 %** |
| M10-3 | MUNDO_FIJO razón **[0.8, 1.3]**: pasa si es evaluable (el mundo sin cambios no regala acumulación, porque tampoco hay casi nada que acumular). | pasa **60 %**; n/a **30 %** |
| M10-4 | pasa (ya medido en el arnés: 77/79 → 79/79 tras corregir el eco del nodo). | **97 %** |
| COSTE | celdas MAPA/NADA **[1.0, 1.4]** (el mapa hace vivir más → más divisiones); muertes **[0.4, 0.9]**. Puede caer por celdas. | pasa **55 %** |
| **Paquete entero** | | **≤ 5 %**. Lo que espero declarar: **el mundo exige lo que el encargo pide (se agota, hay alias, saber dónde cuenta: MAPA > REL) y el organismo del tronco NO lo cruza con sus reglas locales** — el resultado "para y dilo" del §8. |
Refutadores de la hipótesis H10: R₀(MAPA) ≤ R₀(REL) en A₁₂ ≥ 0.65 (saber DÓNDE no aporta con este mapa) → H10 cae por el mecanismo; R₀(MAPA) ≈ R₀(SITIO_BARAJADO) → el sitio del mensaje no es lo que actúa.

## 6. Humo (UN proceso, 6 corridas de T = 100 000, semillas ya vistas 1 y 2: NADA s1, MAPA s1, REL s1, INMORTAL s1, NODO_BARAJADO s1, MAPA s2; escribe `datos/humo/mundo_fase10_humo_<sello>.json` y lo relee)
Predicciones HH escritas en el runner antes de correrlo: **HH1** ancla con una semilla (NADA ∈ [0.05, 0.45], INMORTAL ∈ [0.5, 2.0]; se reporta) · **HH2** el mundo se agota (agotados > 0 y vida de sitio ≤ T/4 en las 6; **bloquea**) · **HH3** MAPA vive más y R₀ mayor que NADA (s1) · **HH4** MAPA > REL en R₀ (s1) · **HH5** MAPA > NODO_BARAJADO (s1) · **HH6** instrumento: contabilidad, sitios_leidos > 0, lect_div > 0, alias > 0 (**bloquea**). Si HH3–HH5 caen se escriben aquí y la serie corre con esta letra; ningún umbral se toca después del humo (regla 4).

## 7. Las cuatro trampas
1. **Canal simétrico** — el que muere escribe (patrón, R, necesidad, **sitio**), el que nace lee; nadie se lee a sí mismo (`_nodo` se llena al morir, se lee al nacer). Controles: NODO_BARAJADO (contenido), SITIO_BARAJADO (dónde), SIN_HERENCIA (canal escrito y no leído).
2. **Acierto sin balancear** — se reporta **J = p1 + c1 − 1** por brazo junto a R₀; la cobertura de M10-2 cuenta sólo mordidas con **R > 0** (comer, no evitar) y R₀ castiga morir de hambre.
3. **El mundo que se come la comida** — `exposiciones` por brazo con mínimo 0.5× NADA (SEG); los sitios se abren con el rng del mundo, igual para todos los brazos; **los tipos "malo" y "bueno" se mantienen 4/4 por construcción** (flips y viradas en pares), para que ningún brazo vea un mundo más pobre. Se reporta `muertes_nec` [energía, agua].
4. **Sitios fijos que se memorizan** — posiciones, patrones, valencias y viradas **sorteados por semilla con rng propio**; ningún sitio dura más de 25 bocados; el recién nacido nace en `rng.integers(L)`.

## 8. Fallos pasados que este diseño podría repetir y cómo los evita (líneas del REGISTRO auditadas; borrador del aprendiz 04 reescrito)
| ERR | por qué este diseño podría repetirlo | comprobación concreta |
|---|---|---|
| ERR-35 (`REGISTRO:4559`) preguntar al mundo lo que no contiene / recalibrar tras ver datos | el mundo podría ser tan duro que **nadie** cruza (ni INMORTAL), y la tentación sería aflojar después del humo | el techo se mide **antes**: INMORTAL es la cota superior y su ancla [0.8, 1.3] es bloqueante (M10-0); las sondas de calibración están declaradas en §2 y el humo no toca umbrales |
| ERR-36 (`REGISTRO:4597`) / E-04 fuga de semilla | sitios, patrones y cambios sorteados podrían consumir el rng del organismo y volver incomparables los brazos | rng propio del mundo (880000+…), del barajado de sitios (890000+…); el constructor comprueba con regex que ninguna línea nueva consume `rng.`; I1/I2/I3 del arnés |
| ERR-38 (`REGISTRO:4811`) / ERR-41 batería copiada con parámetros mudos; perilla inerte | el mapa con visión ilimitada es inerte; `nodo_tabla=0` sin `nodo_sitio` no haría nada; un control podría ser NADA disfrazado | I4 predice y comprueba la inercia; guardias que abortan; D1–D12 "deben diferir" (12/12 en el arnés); `frac_div` y `sitios_leidos` > 0 en SEG; CUERPO campo a campo con `corre_f9.CUERPO` (I7) y defaults de mundo_mapa explícitos |
| ERR-42 (`REGISTRO:4842`) JSON nunca escrito, sintaxis sin compilar | el runner construye 12 brazos con `dict(**)`: un kwarg repetido rompe al importar (**me pasó**: `cambio10` duplicado en MUNDO_FIJO, 20:19; corregido antes del humo) | `py_compile` en el constructor; el humo escribe su JSON y lo **relee** con `lee_json` antes de dar veredicto |
| ERR-54 (`REGISTRO:5311`) crudo perdido tras el análisis | puertas nuevas con claves que pueden no existir (`cob_g5` None) | el crudo se escribe antes de `puertas()`; las medianas toleran None |
| ERR-60 (`REGISTRO:5351`) semillas de hijos que colisionan | rng de hijos 700000+1000000·seed+k ya existía; añado dos rng nuevos | offsets 880000 y 890000 distintos de todos los existentes (700000, 800000, 850000, 860000, 870000) |
| ERR-62 (`REGISTRO:5366`) el hijo nace vacío y muere antes de aprender | es **la** hipótesis nula de este mundo | por eso el candidato transmite QUÉ y DÓNDE y por eso predigo que aun así cae (§5) |
| ERR-87 (`REGISTRO:5493`) leer "el último JSON" por prefijo | dos humos el mismo minuto | `lee_json(carpeta, prefijo, sello)` con sello exacto |
| ERR-89 (`REGISTRO:5587`) puerta sin línea impresa | 8 puertas y 12 brazos: fácil dejar una sin imprimir | `puertas()` imprime exactamente una línea por clave de UMBRALES |
| ERR-91 (`REGISTRO:5757`) umbral igual al nulo; A₁₂ ≥ 0.50 pareado | la razón gen5/gen1 tiene nulo 1.0 | nulo, margen y n declarados por puerta (§4); brazo PLACEBO; A₁₂ ≥ 0.85 |
| ERR-92/93 (`REGISTRO:5773, 5980`) ancla calibrada con pocas series | el ancla del mundo 10 nace con 4 semillas de sonda | se declara así; la regla de recalibración es la de ERR-93b (`[0.75·mín, 1.25·máx]` unido al vigente, nunca estrechar) para la réplica |
| E-10/ERR-33 condición manipulada 0 veces | un tipo podría no virar nunca en una corrida | `cambios_por_tipo` en el crudo; mínimo reportado en SEG (16 viradas entre 8 tipos: esperadas 2 por tipo) |
| E-14 pocos eventos por brazo | cuerpos de generación ≥ 5 pueden ser un dígito | umbral MIN_G5 = 10 declarado; si no, la puerta es NO EVALUABLE, no "pasa" ni "cae" |
| E-17 los rivales ven la etiqueta verdadera | el ORÁCULO ve la tabla verdadera | se declara como cota superior de QUÉ, no como rival; tabla "qué ve cada brazo": todos ven la misma retina, el mismo mundo, el mismo rng del mundo; sólo cambia lo que el nodo entrega al nacer |

## 9. Lo que NO se declara
"Población", "cultura", "enseña", "entiende", "planifica". Más de un cuerpo a la vez no está construido. La "generación" es un contador de partos. Si MAPA cruza M10-1, lo que se declara es "el linaje que recibe QUÉ y DÓNDE del nodo se sostiene en este mundo", no "la transmisión es acumulativa" hasta que M10-2 y M10-3 pasen y se repliquen en 2421–2440.

## 10. Arnés — salida pegada entera (`python identidad_mundo_fase10.py 20000`, 20:24–20:29, UN proceso; sha del arnés `93ee2dd48f1f664f`, de la salida `74e3f3ae45e9b5af`)
Primera pasada (20:21) 77/79: I5 marcaba diferencia por el eco de configuración del nodo (`curitas`, `nodo_n`, `nodo_cola`, `alma_cfg`; conducta idéntica) y el comparador sólo ignoraba `extra` a un lado. Se corrigió el **comparador del arnés**, no el organismo ni el mundo. Segunda pasada:

```
IDENTIDAD mundo_fase10  (sha 48b11724a4e70842; este arnes 93ee2dd48f1f664f)
  sha 3a821884394d66c9  organismo_f9.py (origen)
  sha 17528d767fcebaf6  organismo_v142.py (TRONCO)
  sha feefc88b1fd8d434  organismo_v14.py (v14.1)
  sha 207d6a1954336b18  mundo_mapa.py
  sha 839fa71f9c84cb26  organismo_vivo_codigo.py
  T = 20000 · semillas (1, 2) · un proceso, sin Pool

(I7) REGLA 14 -- campo a campo. CUERPO de este arnes vs corre_f9.CUERPO:
  diferencias: NINGUNA   CUERPO = {"costo": 0.001, "costo_a": 0.001, "dote": 0.6, "estims": ["A", "B", "C", "D"], "h1": 1, "hereda": "nada", "muerte_real": 1, "n_nec": 2, "rep2": 1, "rep2_regalo": 600, "rep_X": 500, "rep_coste": 0.0, "rep_cuello": 2, "rep_mide": 1, "rep_umbral": 1.0, "reproduccion": 1, "vivo": 1}
  MUNDO 10 (perillas del mundo, no del cuerpo) = {"L10": null, "cambio10": 12500, "desambiguar": 1, "estims": null, "f10": 1, "flip10": 1, "mundo10": 1, "nfam10": 4, "npx": 9, "nsit10": 6, "nvar10": 2, "r_vis": 8, "regen10": 50, "stock10": 25}   MAPA = {'usa_M': 1, 'nodo_sitio': 1, 'escribe_M': 1, 'gamma_M': 0.6, 'H_M': 20, 'disc_M': 0.9}
  I2 usa la letra de identidad_v142.ESC (12 escenarios): ['AB por defecto', 'AB invertido', 'AB + patron nuevo C', 'AB solap_AB=3 (E2L)', 'AB sin plasticidad', 'AB via lenta apagada', 'AB sin puerta', 'AB sin division por signo', 'AB sin hija dispersa', 'AB sin puerta por codigo', 'AB las dos perillas v14 off', 'AB D comida solap_B=2 (E2K)']

(I1) APAGADA: mundo_fase10 == organismo_f9 en los 9 brazos de corre_f9 (claves viejas; nuevas solo B-5 de solo lectura)
  [   4.4s] (I1) RENACE                                                                          2/2 IDENTICO
  [   8.8s] (I1) NADA                                                                            2/2 IDENTICO
  [  13.3s] (I1) M1                                                                              2/2 IDENTICO
  [  20.1s] (I1) REC                                                                             2/2 IDENTICO
  [  27.6s] (I1) REL                                                                             2/2 IDENTICO
  [  33.6s] (I1) REL_FIJO                                                                        2/2 IDENTICO
  [  42.8s] (I1) REL_BAR                                                                         2/2 IDENTICO
  [  50.1s] (I1) REL_AZAR                                                                        2/2 IDENTICO
  [  58.2s] (I1) REL_TARDE                                                                       2/2 IDENTICO

(I2) TRONCO: mundo_fase10(vivo=0, n_nec=1, desambiguar=1) == organismo_v142 en los 12 escenarios de identidad_v142 (TODAS las claves)
  [  63.7s] (I2) AB por defecto                                                                  2/2 IDENTICO
  [  68.8s] (I2) AB invertido                                                                    2/2 IDENTICO
  [  74.1s] (I2) AB + patron nuevo C                                                             2/2 IDENTICO
  [  79.4s] (I2) AB solap_AB=3 (E2L)                                                             2/2 IDENTICO
  [  84.8s] (I2) AB sin plasticidad                                                              2/2 IDENTICO
  [  89.9s] (I2) AB via lenta apagada                                                            2/2 IDENTICO
  [  94.8s] (I2) AB sin puerta                                                                   2/2 IDENTICO
  [ 100.0s] (I2) AB sin division por signo                                                       2/2 IDENTICO
  [ 105.3s] (I2) AB sin hija dispersa                                                            2/2 IDENTICO
  [ 110.0s] (I2) AB sin puerta por codigo                                                        2/2 IDENTICO
  [ 115.1s] (I2) AB las dos perillas v14 off                                                     2/2 IDENTICO
  [ 120.7s] (I2) AB D comida solap_B=2 (E2K)                                                     2/2 IDENTICO

(I3) el rng NO se consume: T=120000 == organismo_v142
  [ 136.8s] (I3) T=120000 s1                                                                     1/1 IDENTICO

(I4) PREDICCION: el mapa con vision ilimitada es INERTE en el mundo vivo del tronco (usa_M=1, r_vis=None == usa_M=0)
  [ 143.2s] (I4) NADA vivo usa_M=1 r_vis=None == usa_M=0                                         2/2 IDENTICO

(I5) SIN_HERENCIA == NADA en el mundo 10 salvo las claves del nodo (el nodo se escribe, nadie lo lee)
  [ 150.2s] (I5) SIN_HERENCIA == NADA (mundo 10)                                                 2/2 IDENTICO

(I6) DETERMINISMO: dos llamadas iguales (MAPA, mundo 10)
  [ 166.9s] (I6) MAPA == MAPA                                                                    2/2 IDENTICO

(D) CONTROLES QUE DEBEN DIFERIR (mundo 10)
  [ 173.2s] (D1) mundo10=1 != mundo10=0 (NADA)                                                   2/2 DIFIERE (como debe)
  [ 179.5s] (D2) cambio10=12500 != cambio10=0 (MUNDO_FIJO)                                       2/2 DIFIERE (como debe)
  [ 186.1s] (D3) REL != NADA                                                                     2/2 DIFIERE (como debe)
  [ 197.8s] (D4) NODO_BARAJADO != REL                                                            2/2 DIFIERE (como debe)
  [ 205.2s] (D5) ORACULO_SIN_MAPA != REL                                                         2/2 DIFIERE (como debe)
  [ 217.6s] (D6) MAPA != REL (sin mapa)                                                          2/2 DIFIERE (como debe)
  [ 232.6s] (D7) MAPA_SIN_TABLA != MAPA                                                          2/2 DIFIERE (como debe)
  [ 249.2s] (D8) SITIO_BARAJADO != MAPA                                                          2/2 DIFIERE (como debe)
  [ 256.8s] (D9) PLACEBO (placebo=1) != tronco (NADA mundo 10)                                   2/2 DIFIERE (como debe)
  [ 264.0s] (D10) INMORTAL != NADA                                                               2/2 DIFIERE (como debe)
  [ 271.7s] (D11) desambiguar=1 != 0 en el mundo 10 (B-5 actua)                                  2/2 DIFIERE (como debe)
  [ 277.4s] (D12) s1: lect_div REL 9/9 · sitios leidos MAPA 695 · M llenas al final 6 · des_splits NADA(B-5) 18
  [ 286.1s] (D12) s2: lect_div REL 28/28 · sitios leidos MAPA 2279 · M llenas al final 11 · des_splits NADA(B-5) 13

(G) GUARDIAS -> SystemExit
  OK    guardia: mundo10 con vivo=0
  OK    guardia: mundo10 con estims
  OK    guardia: nodo_sitio sin usa_M
  OK    guardia: usa_M sin r_vis en el mundo 10
  OK    guardia: nodo_tabla=0 sin nodo_sitio

ARNES identidad_mundo_fase10: 79/79 en 288s
VEREDICTO identidad_mundo_fase10: PASA
```

## 11. Humo — resultado (20:19–20:21; `datos/humo/mundo_fase10_humo_20260921_201914.json`, sha `b4cdef09e840a3fe`; `python corre_mundo_fase10.py --humo`)
| brazo · semilla | R₀ | r | vida | cuerpos | fund. | muertes [E, Ag] | J | saciedad | gen máx | cuerpos g≥5 | agotados | vida de sitio | alias | cambios | sitios leídos | celdas | div. B-5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NADA s1 | **0.111** | −407 | 82 | 459 | 407 | [41, 417] | 0.033 | 0.369 | 4 | 0 | 60 | 3202 | 0.505 | 14 | 0 | 30 | 66 |
| MAPA s1 | **0.237** | −192 | 127 | 253 | 196 | [70, 182] | 0.369 | 0.377 | 5 | 6 | 38 | 2876 | 0.520 | 14 | 12 495 | 41 | 61 |
| REL s1 | **0.503** | −90 | 111 | 183 | 90 | [92, 90] | 0.427 | 0.576 | 6 | 37 | 71 | 2640 | 0.511 | 14 | 0 | 30 | 68 |
| INMORTAL s1 | **0.915** | −8 | 200 | 106 | 0 | [16, 89] | — | 0.592 | 1 | 0 | 65 | 2750 | 0.0 | 14 | 0 | 49 | 12 |
| NODO_BARAJADO s1 | **0.245** | −175 | 108 | 233 | 182 | [58, 174] | 0.029 | 0.463 | 3 | 0 | 46 | 3638 | 0.522 | 14 | 11 468 | 32 | 101 |
| MAPA s2 | **0.294** | −141 | 181 | 201 | 148 | [106, 94] | 0.220 | 0.415 | 3 | 0 | 52 | 2937 | 0.575 | 14 | 9 779 | 37 | 54 |

**HH:** HH1 SÍ (ancla en rango con una semilla: NADA 0.11, INMORTAL 0.92) · HH2 SÍ (el mundo se agota: 38–71 sitios agotados por corrida, vida de sitio 2 640–3 638 ≤ 25 000) · HH3 SÍ (MAPA vive más y R₀ > NADA) · **HH4 NO** (REL 0.503 > MAPA 0.237: saber DÓNDE por este mapa **empeora**; saciedad 0.58 vs 0.38) · **HH5 NO** (MAPA 0.237 ≈ NODO_BARAJADO 0.245: en el brazo con mapa el contenido del nodo no es lo que actúa) · HH6 SÍ (contabilidad 5/5 mortales; sitios leídos 9 779–12 495; lect_div > 0; alias 0.51–0.58).
**Lo que el humo refuta antes de la serie (declarado, sin tocar umbrales):** (1) el candidato MAPA no es mejor que REL: el sesgo de dirección de `mundo_mapa` (γ 0.6, H 20) alimentado con los sitios del nodo lleva al cuerpo a sitios que ya se agotaron o viraron, y come menos; (2) la medida de cobertura de M10-2 es **degenerada** (mediana 0.0 en MAPA y REL: la mayoría de los cuerpos muere sin morder nada con R > 0; y puede pasar de 1, INMORTAL 1.5, porque el numerador acumula a través de viradas y el denominador es "útil ahora") — M10-2 no se puede leer con esta letra: se declara y se propone la medida corregida (cobertura por ventana entre viradas) para el preregistro siguiente, con ERR numerado por el coordinador; (3) el mejor brazo mortal (REL, 0.50) está en el mismo techo que el ORÁCULO de la fase 9 (0.51/0.56): **con este mundo y este organismo, el muro sigue siendo el mundo** — el cuerpo nuevo con el nodo por relevancia sabe QUÉ en su primer encuentro (J 0.43 vs 0.03) y aun así muere de sed/hambre antes de reproducirse.
**Consecuencia para la serie:** la serie confirmatoria con esta letra costaría ~1 h de Pool 7 para confirmar dos puertas que el humo ya predice caídas (M10-1, M10-2). Recomiendo NO gastarla tal cual (PODERES §1.2: "si en el humo no aparece la señal, no sigas") y llevar al coordinador el diseño del mundo (que sí cumple §2.1.1, .3, .6 y probablemente .2 y .4) con dos cambios preregistrados aparte: (a) el DÓNDE debe entrar por una vía que no sea el sesgo difuso de nivel 6 (ya medido "no rodea fiable", ENCARGO §7), o el mapa se descarta y se mide REL solo con más `nodo_lee`; (b) medida de acumulación por ventana. Si el coordinador prefiere correrla igual, el comando es el de la cabecera y la letra es la de §4.

## 12. Semillas usadas por mí (sólo sondas y humo, un proceso): 1, 2, 3, 4 (ya vistas en JUACO; T ≤ 100 000). Las de la serie (2401–2440) no se han tocado.
