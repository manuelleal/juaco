# PREREGISTRO — NIVEL 6, BLOQUE "SUBIDA_N6B": dos metas en el mundo partido, mapa completo, sobre el tronco v14.2

**23-sep-2026. Creador de la tanda 2 del nivel 6 (Opus). Escrito ANTES del humo.** Lo único corrido antes de escribir
esto: el arnés de identidad (dos pasadas, §9), tres corridas de depuración en semillas del arnés (14643, 14644) y un
perfilado de 20 000 pasos (14642). Ninguna usa semillas de serie, réplica ni humo. Las predicciones de §5 se firman
**antes** del humo; los números del humo se agregan en §10 sin tocar §4–§8.

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños
preregistrados con controles y réplicas).

## 1. De dónde sale (subida_n6, REGISTRO "SUBIDA N6", 23-sep)
GF (gradiente + filtro sobre la tabla M) rodeó limpio 1.0 / 0.925 en serie y réplica; los controles dieron 0. Cayó
V1: la memoria no tenía la comida y las dos murallas enteras en 1 y 5 semillas. **Hallazgo al releer el JSON sellado de
la réplica** (`af98c6148285a2be`): V1 no es sólo validez. En 6629 (6/21 venenos en M), 6632 (16/21) y 6639 (12/21) GF
rodeó **0.0**: el campo se escapa por la muralla que no recuerda. La mediana lo tapó. Además faltan, según su §10,
dos metas en 2D, el port a v14.2, el mapa corregido dentro del episodio y los rodeos compuestos.
**Este bloque ataca tres de los cinco a la vez:** V1 (mapa completo), dos metas en 2D y el port a v14.2.

## 2. Hipótesis
**H.** El **tronco v14.2**, en un mundo 2D partido por veneno con un solo cruce, logra tres cosas:
- si explora cuando está **saciado**, completa su mapa: las dos comidas y las dos murallas en M, en 20/20 semillas;
- con ese mapa, leído por GF, **elige entre dos comidas recordadas la más cercana por camino, no por línea recta**;
- llega a ella **sin pisar** el veneno.

Hay dos clases de salida, balanceadas:
- *cruza*: la correcta está al otro lado, así que hay que rodear por el hueco;
- *desvía*: la correcta está del mismo lado, y la del otro lado queda más cerca en línea recta. Es una trampa.

**H0-BRÚJULA.** Lo hace porque sabe dónde están las comidas, no porque recuerde que el veneno corta el paso.
**H0-GF.** Explorar no hace falta: GF sin explorar ya elige y rodea igual.

## 3. Mecanismo mínimo, memoria nueva y mundo
**Memoria nueva persistente: CERO. Constantes nuevas: CERO.** Todo vive en la misma tabla M `(posición → último
patrón visto)`.

- **explora** (el candidato). Actúa sólo si hay saciedad (`hambre == 0`, o sea `E ≥ 1`) y la retina está vacía.
  - Suma `gamma_M` (la constante del mapa) hacia cada celda vecina que M no conoce.
  - Con hambre no explora: lee el campo como en subida_n6.
  - La celda pisada y vacía queda conocida en M, con patrón vacío. `_campo` salta lo vacío y `valor()` no se consulta
    sobre ello.
  - En la prueba `E_test = 0.3`, así que `hambre = 0.7` y explora **no actúa**: la prueba mide la lectura, no la
    exploración.
  - Referencia: aprendizaje latente (Tolman y Honzik 1930; Tolman 1948).
- **vista** (reportada, no candidata). M se escribe también con lo que la retina ve a un paso (`d == 1`: la celda es
  exacta). Referencia: células de vector de objeto (Høydal et al. 2019, *Nature* 568:400).
  - Depuración (semilla del arnés 14644, T = 100 000): **la vista sola no completó el mapa**. Hubo 523 avistamientos a
    un paso, todos de celdas ya conocidas, porque el organismo sólo iba y venía a una comida: M tenía 1/2 comidas y
    6/21 venenos, y el resultado fue bit a bit igual sin la vista a T = 20 000. De ahí sale explora.
- **Organismo:** TRONCO v14.2. Se copia el delta v13 → v14.2 de `organismo/organismo_v142.py` (`17528d767fcebaf6`,
  congelado, sólo se lee) sobre `experimentos/subida_n6/mundo_subida.py` (`484e34db8f2150da`).
  - 12 trozos, cada uno verificado tal cual en el tronco.
  - El runner lee los kwargs del tronco con `inspect`: `eta_s 0.15`, `clip_s 10`, `mask_rel 2`, `puerta_pat 5`,
    `pat_min 1`, `desambiguar 1`. Aborta si difieren de lo declarado.
- **Mundo D (principal).** Toro 11 × 11 con dos murallas: la fila 0 con UN hueco y la fila −5 entera (`cierre`, el de
  subida_n6). Además:
  - `r_vis = 1`, `regen = 50`, `T = 100 000`;
  - DOS comidas: A1 en la banda de arriba y A2 en la de abajo;
  - 40 episodios (20 *cruza* y 20 *desvía*, alternados), `max_pasos = 60`, sin aprendizaje ni boca.
  - Las salidas salen de un BFS sobre el mundo REAL (instrumento): margen de camino ≥ 2 y camino a la correcta ≤ 18
    (`H_M = 20` ondas).
  - La geometría se sortea con el rng de la geometría (`1000003·seed + 7`, no el del organismo). Se exigen ≥ 3
    salidas de cada clase. La primera tirada es la de subida_n6.
  - **Declarado:** la condición rechaza muchas tiradas (arnés: 14, 51 y 47 intentos) y deja 3–4 salidas *cruza*
    distintas y 8–10 *desvía* por semilla, que se repiten en ciclo. El ruido motor (`N(0, 0.3)`) hace distinto cada
    episodio.
- **Mundo P (puerta de port):** el mundo de subida_n6 sin cambios (una comida, rodeo/atajo).

**Anclas y sha:**

| archivo | sha |
|---|---|
| `construye_subida_b.py` | `35ea55d76638aabc` |
| `mundo_subida_b.py` | `214d5763758473fa` |
| `identidad_subida_b.py` | `2f29aef761459521` |
| `corre_subida_b.py` | `a353caf2b1302eaf` |

El runner verifica el sha del mundo y del tronco. **Regla 14:** compara campo a campo CIEGO, GF, GFX, UNA y GFX_13
contra `subida_n6/corre_subida.kw_de` (`374846482660917d`). Sólo difieren los kwargs del tronco,
`prueba.metas2/min_salidas/margen/p_max` y `explora`. Aborta ante banderas desconocidas o abreviadas (ERR-115) y ante
semillas fuera de 14601–14640.

**Brazos (11 × 20 semillas):**

| brazo | qué es |
|---|---|
| CIEGO | sin mapa |
| GF | la lectura de subida_n6 |
| GFV | GF + vista |
| **GFX** | **candidato:** GF + explora |
| GFVX | GF + vista + explora |
| BRÚJULA | GFX, pero el veneno recordado no bloquea el campo |
| BARAJADO | GFX con barajar |
| INVERTIDO | GFX con invertir |
| PLACEBO | GFX + 3 sorteos descartados |
| GFX_13 | GFX sobre v13 (reportado) |
| UNA | GFX en el mundo P (puerta de port) |

## 4. Puertas (mediana de 20 semillas; «media» = (limpio(cruza) + limpio(desvía)) / 2 por semilla)
| # | puerta | medida | umbral |
|---|---|---|---|
| D-1a | cruza: elige la del otro lado y rodea | limpio(cruza) de GFX | ≥ 0.60 |
| D-1b | desvía: elige la del mismo lado | limpio(desvía) de GFX | ≥ 0.60 |
| D-2 | balanceada | J = D-1a + D-1b − 1 | ≥ 0.50 |
| D-3 | es el veneno recordado | media GFX − BRÚJULA | ≥ 0.25 |
| D-4 | es el mapa | media GFX − máx(CIEGO, BARAJADO) | ≥ 0.25 |
| D-5 | no es huida | huye(cruza) de GFX | ≤ 0.20 |
| R-4 | no regresión | comida GFX / CIEGO | ≥ 0.90 |
| R-5 | muertes | GFX / máx(CIEGO, 1) | ≤ 1.25 |
| C1 | decisivo | media de INVERTIDO | ≤ 0.20 |
| PLACEBO | instrumento | \|media GFX − PLACEBO\| | ≤ 0.15; si no, **no se lee** |
| **V1** | **memoria completa** | 2/2 comidas y 21/21 venenos en M de GFX | **20/20** |
| PORT-a | v14.2 rodea en el mundo de subida_n6 | limpio(rodeo) de UNA | ≥ 0.60 |
| PORT-b | ídem, balanceado | J de UNA | ≥ 0.50 |

Núcleo: D-1a, D-1b, D-2 y D-3.

Se reportan sin ser puerta:
- GF, GFV, GFVX y GFX_13;
- V1 de cada brazo;
- `a_la_otra(desvía)` de BRÚJULA, para ver si la trampa funciona;
- los pareados GFX > BRÚJULA y GFX > GF (k/20);
- el subconjunto de la regla 10, que no cambia la letra.

**Nulo del margen (regla 15): no verificado.** No hay serie del nulo. PLACEBO (tope 0.15) queda por debajo de los
márgenes 0.25.

## 5. Predicciones (firmadas antes del humo)
1. **GFX:** limpio(cruza) **0.80–1.00** (punto 0.95); limpio(desvía) **0.80–1.00** (0.95); J 0.60–1.00; huye ≤ 0.05.
2. **V1 de GFX: 18–20/20** (punto 20). **Es la que puede fallar:** la letra pide 20/20 y le doy p ≈ 0.6.
3. **GF sin explorar:** V1 **≤ 8/20** y media **0.30–0.75**. GFX > GF en **≥ 12/20** semillas. Así, completar el
   mapa se ve en la conducta y no sólo en la validez.
4. **GFV:** V1 ≤ 10/20 (la vista sola no basta). **GFVX dentro de ±0.10 de GFX:** la vista sobra y el mecanismo
   mínimo es explora. Si GFVX le gana a GFX por > 0.10, lo digo.
5. **BRÚJULA:** limpio(cruza) 0.00–0.20, limpio(desvía) 0.00–0.30, `a_la_otra(desvía)` ≥ 0.50. D-3 con margen
   0.60–1.00.
6. **Controles:**
   - CIEGO: media 0.00–0.15;
   - BARAJADO: 0.00–0.40 (riesgo de §6);
   - INVERTIDO: ≤ 0.10;
   - PLACEBO: dentro de ±0.10 de GFX;
   - GFX_13: dentro de ±0.10 de GFX.
7. **R-4:** GFX come 500–1 000 (depuración: 704 y 748); CIEGO 250–600. Razón **1.2–3.5**. Puede caer: explorar
   saciado cuesta comida (GFV comió 1 963 en la depuración).
8. **R-5:** GFX 0–5 muertes; CIEGO 50–200 (subida_n6: 140).
9. **PORT:** UNA limpio(rodeo) 0.85–1.00 y J 0.70–1.00.

## 6. Controles que pueden ganar y qué refuta
- **GF sin explorar es el control que puede ganar.** Si su media queda a ≤ 0.05 de GFX y su V1 llega a ≥ 18/20,
  explorar no hacía falta: **H0-GF en pie** y se refuta la parte "completar el mapa" de H.
- **BRÚJULA:** si D-3 < 0.25, lo que elige es saber dónde están las comidas, no que el veneno corta: **H refutada**.
  Que `a_la_otra(desvía)` salga alta en BRÚJULA confirma que la trampa separa las dos lecturas.
- **Refutan H además:** D-1a o D-1b < 0.60, J < 0.50, C1 > 0.20, o huye > 0.20.
- **BARAJADO bajo lectura por signo:** en subida_n6 conservó el mapa en 6/20 semillas de la serie. Si D-4 cae por eso,
  cae por la letra y no se reinterpreta.
- **Port:** si PORT-a o PORT-b caen, el tronco v14.2 no hereda el rodeo de v13 en ese mundo.

## 7. Las cuatro trampas (más la quinta)
1. **Canal simétrico:** no hay canal. Las dos clases son simétricas por construcción: hay salidas en las dos bandas.
2. **Acierto sin balancear:** las dos clases, 20 y 20, se juntan en J. Una heurística "voy a la de mi lado" da J = 0;
   "voy a la más cercana en recta", también.
3. **Mundo que se come la comida:** `regen = 50`. Cada episodio restaura `objs`, M, E y la traza. Explora cambia la
   vida, y por eso R-4 y R-5 son puertas.
4. **Sitios fijos:** hay geometría por semilla con rng propio, origen azaroso y espejo por paridad. Está condicionada
   (declarado en §3).
5. **ERR-117 (toro que no se parte):** el arnés comprueba con un BFS independiente, en cada semilla, que el mundo
   queda partido en dos bandas más el hueco, y clasifica cada salida.

## 8. Criterio, vocabulario y puntos (propuesta; decide el director)
- **FUNCIONA:** 13/13 principales en serie **y** réplica, con la misma letra.
  - Propuesta: **nivel 6 → 80 %**.
  - Porqué: el núcleo de subida_n6 sube a su FUNCIONA (V1 completo, 70 %), más dos metas en 2D (+5), más el port a
    v14.2 (+5). Lo que queda del 100 % es el mapa corregido dentro del episodio (hueco que se mueve: desdecirse, 10)
    y los rodeos compuestos más allá de `H_M` (10).
  - Vocabulario: *«en un mundo 2D partido por veneno recordado con un solo cruce, el tronco v14.2, tras explorar
    saciado hasta tener el mapa completo, elige entre dos comidas recordadas la más cercana por camino (no la más
    cercana en línea recta) y llega sin pisar el veneno; si el veneno recordado no corta el campo, pisa la
    muralla»*.
- **HAY ALGO MODESTO:** el núcleo pasa en serie y réplica pero cae otra principal. Propuesta: **65–70 %** (70 si lo
  único que cae es V1 o R-4).
- **NO:** el núcleo cae en la serie. El nivel no cambia.
- **Prohibido:** «planifica», «entiende el espacio», «curiosidad», «aprende el mapa»; M se escribe, no se aprende por
  error. También «elige» sin la trampa al lado.

## 9. Lo corrido antes de escribir esto
- **Arnés `identidad_subida_b.py`, primera pasada: 74/75.** Cayó el control «vista = 1 difiere» en 14644: fue bit a bit
  igual, y la depuración de §3 explica por qué.
  - Arreglo **antes del humo**: la vista se prueba con explora encendida.
  - Segunda pasada: **RESULTADO: 75/75**. Salida en `identidad_subida_b_salida.txt`; JSON
    `datos/humo/identidad_subida_b_20260923_182811.json` (`bed318363156a827`).
  - Contenido del arnés:
    - 45 identidades I-13 contra mundo_subida: anillo v13, mapa, 2d, rodeo, los 5 brazos del 21-sep y los 6 del mundo
      partido de subida_n6;
    - 9 identidades I-142 contra `organismo_v142.run` (por defecto, `invertir_en` y `nuevo = C`);
    - 15 controles que deben diferir;
    - 6 revisiones de clases con un BFS independiente.
- **Depuración (semillas del arnés, T = 100 000; no es dato):**

  | semilla | brazo | limpio cruza / desvía | M comidas | M venenos | comida | segundos |
  |---|---|---|---|---|---|---|
  | 14644 | GFV | 1.0 / 0.45 | 1/2 | 6/21 | 1 963 | 17 |
  | 14644 | GFVX | 0.95 / 1.0 | 2/2 | 21/21 | 748 | 50 |
  | 14643 | GFX | 1.0 / 1.0 | 2/2 | 21/21 | 704 (1 muerte) | 50 |

  Perfil a 20 000 pasos: el costo está en `_campo`, que se recalcula en cada pisada sobre un objeto (código heredado).
  Vectoricé el salto de lo vacío; el resultado fue idéntico.

## 10. Humo (agregado DESPUÉS; §4–§8 no se tocaron; una semilla, no se interpreta)
`python experimentos/subida_n6b/corre_subida_b.py --humo`: semilla 14641, T = 100 000, 6 corridas, un proceso, 229 s.
JSON `datos/humo/subida_b_humo_20260923_183110.json` (`0377b2a258056ea2`).

| brazo | limpio cruza / desvía | a_la_otra (desvía) | M comidas | M venenos | comida | muertes | segundos |
|---|---|---|---|---|---|---|---|
| CIEGO | 0.0 / 0.05 | — | — | — | 1 240 | 6 | 17.6 |
| GF | 1.0 / 0.75 | — | 1/2 | 18/21 | 1 953 | 2 | 12.6 |
| **GFX** | **1.0 / 0.95** | — | **2/2** | **21/21** | **685** | **2** | 43.8 |
| BRÚJULA | 0.0 / 0.0 (pisa 1.0 / 1.0) | **1.0** | — | — | — | — | 57.8 |
| INVERTIDO | 0.0 / 0.0 | — | — | — | — | — | 48.0 |
| UNA (mundo P) | 1.0 / 0.95 (rodeo / atajo) | — | 1/1 | 21/21 | 601 | — | 49.3 |

Con 6 de 11 brazos, 11/13 puertas pasan:
- **R-4 cae**: comida GFX / CIEGO = 685 / 1 240 = **0.552**;
- PLACEBO no se corrió.

**Predicción 7 refutada ya en el humo:** puse CIEGO 250–600 y razón 1.2–3.5.
- Con dos comidas densas, el ciego come 1 240.
- Explorar saciado le cuesta a GFX la mitad de la comida que come GF (685 contra 1 953), sin costarle vidas.
- R-4 **no se enmienda**: moverla después de ver el humo sería candidato a ERR.
- Lectura previa, declarada: lo más probable es que R-4 caiga en la serie. En ese caso el techo por la letra es
  **HAY ALGO MODESTO** (65–70 %, §8).

## 11. Semillas y comandos (los corre el coordinador; un Pool ≤ 6)
**Serie 14601–14620; réplica 14621–14640; humo 14641; arnés 14642–14644.** Verificación:
- `grep` de `146[0-4][0-9]` en `.md`, `.py`, `.txt` y `.log` de `PROYECTOS/JUACO/*` (bundle y los 10 worktrees): sólo
  aparecen conteos dentro de logs de datos;
- las claves `seed`, `semilla(s)` y `desde` de los 506 JSON que contienen esos números: **0 usos como semilla**;
- ningún archivo `_s146xx`.

```
python experimentos/subida_n6b/identidad_subida_b.py                                   # RESULTADO: 75/75
python experimentos/subida_n6b/corre_subida_b.py --desde 14601 --n 20 --pool 6         # serie, 220 corridas
python experimentos/subida_n6b/corre_subida_b.py --desde 14621 --n 20 --pool 6         # réplica (siempre)
python experimentos/subida_n6b/corre_subida_b.py --lee <serie.json> --sello <sha16> --lee_replica <rep.json> --sello_replica <sha16>
```

**Costo**, medido con otros Pools en la máquina:
- ~50 s por corrida en los 8 brazos con explora y ~17 s en los 3 sin ella.
- Serie: 160 × 50 + 60 × 17 ≈ **9 000 s de CPU (2.5 h)**, **≈ 25–30 min de pared con Pool 6**.
- Réplica: igual.
