# PREREGISTRO — NIVEL 6, BLOQUE "SUBIDA_N6": rodeo en un mundo que SÍ obliga

**23 sep 2026. Creador del equipo del nivel 6 (Opus). Escrito ANTES de la serie.** Lo único corrido: el arnés de
identidad (42/42), un análisis del JSON sellado del 21-sep, cinco corridas de depuración (semilla 6642, del arnés) y
**un humo de 6 corridas (semilla 6641)**. Los números del humo se citan en §9 y NO se interpretan: una semilla.
Las predicciones de §5 se escribieron **después** del humo; se declara.

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños
preregistrados con controles y réplicas).

---

## 1. Lo que hay que saber antes: el mundo del 21-sep no obligaba a rodear (candidato a ERR)

`PREREGISTRO_rodeo_obligado.md` §3 dice: «el toro queda partido en dos mitades y el hueco es el único cruce». **Es
falso.** Una fila de veneno en un toro 11 × 9 no lo parte: un toro sin una fila es un **cilindro**. Desde el arranque
*rodeo* `(fx, −dd)`, cruzar la muralla cuesta `dd + fy` pasos verticales. Dar la **vuelta del toro** (alejarse de la
muralla) cuesta `9 − dd − fy`, y ese camino está limpio. Lo cuenta `analiza_vuelta_toro.py` sobre
`datos/muralla_s1702-1721_20260921_170652.json` (sello `99dc2e86b833fc29`). Salida en `analiza_vuelta_toro_salida.txt`:

| brazo | episodios *rodeo* donde la vuelta del toro es más corta | limpio ahí | rodeo **de verdad** (sólo por el hueco) | limpio ahí |
|---|---|---|---|---|
| CIEGO | 240 de 400 | 0.208 | 160 | **0.006** (1) |
| CAMINO | 240 | 0.517 | 160 | **0.125** (20) |
| BARAJADO | 240 | 0.350 | 160 | 0.062 |
| PLACEBO | 240 | 0.517 | 160 | 0.156 |

Además hay 4 episodios que arrancan **sobre** la comida (`d0 = 0`, con `dd = 5, fy = 4`).
**Relectura:** 124 de los 144 «limpio» de CAMINO salieron de la vuelta del toro. En los rodeos de verdad, el campo
difundido llegó limpio en 0.125. El «huye 0.425» era en parte el camino correcto de ese mundo.
**Propuesta al coordinador: numerar como ERR** («una muralla de una fila no parte un toro; el bloque del 21-sep midió
alejarse, no rodear»). No cambia el veredicto CAE del 21-sep. Sí cambia su lectura: lo que midió como rodeo fue sobre
todo alejarse.

## 2. Diagnóstico analítico: por qué el campo difundido no rodea

1. **La señal es débil.** CAMINO suma `gamma_M·U[vecino]` con `U = v_A·0.9^d`. La diferencia entre el vecino bueno
   y el malo es `0.6·0.9^(d−1)·(1 − 0.81) ≈ 0.114·0.9^(d−1)`, que da 0.055 a `d = 8`. El ruido motor es
   `N(0, 0.3)` por acción. El campo sabe el camino, pero el ruido tapa su voz: por eso tampoco va recto en *atajo*
   (0.25 el 21-sep).
2. **La retina atrae al veneno.** Con `r_vis = 1`, al costear la muralla la retina ve veneno a `d = 1` y deja de
   estar vacía, así que el mapa **se calla justo donde hay que rodear**. `Wl` aprendió a acercarse a lo que ve
   (`Rp = 0.2` por acercarse a cualquier objeto). Costear la muralla es pisarla.

## 3. Hipótesis, mecanismo y mundo

**H.** En un mundo 2D que el veneno recordado **parte de verdad** (un solo cruce, geometría sorteada), la **misma
tabla `M`** lleva al organismo hasta la comida por el hueco **sin pisar el veneno**. Para eso hay que leerla con dos
reglas locales:
- **(grad)** subir por el signo del gradiente local del campo, `gamma_M·sign(U[vecino] − U[aquí])`;
- **(filtro)** el veneno recordado es obstáculo, no objetivo de la retina.

**H0-BRÚJULA.** Lo hace porque sabe dónde está la comida, no porque recuerde que el veneno corta el paso. Esta H0
se pone a prueba con un brazo propio.

**Mecanismo mínimo. Memoria nueva persistente: CERO.** El organismo v13 no cambia: ni `valor()`, ni la boca, ni el
aprendizaje. Todo es lectura de `M` y de `U`, que ya existían. Lo nuevo es:
- `_Nb`, un array derivado (celdas recordadas con `valor < 0`, más una bandera «hay meta») que se recalcula con `U`;
- **grad**, que usa la misma `gamma_M`. Es la regla de frente de onda de Ponulak & Hopfield (2013, *Front. Comput.
  Neurosci.* 7:98): se sigue el gradiente local de una actividad que se propagó entre vecinos;
- **filtro**, que es la memoria de rechazo v9 leída desde `M`. **Sólo actúa si hay meta recordada** (alguna celda
  con `valor > 0`). La depuración mostró por qué hace falta (§9). Actúa en vida y en prueba.

**Mundo PRINCIPAL (P):** toro 11 × 11, `r_vis = 1`, `regen = 50`, `T = 100 000`.
- **Muralla 1:** fila 0 completa menos un hueco.
- **Muralla 2 (`prueba['cierre'] = 5`):** fila −5 completa, sin hueco. Ahora el toro sí queda partido y el hueco es
  el único cruce.
- Hay 21 venenos y una comida en la fila `fy ∈ 1..5`.
- Geometría sorteada por semilla con un rng independiente (`1000003·seed + 7`), más origen azaroso y espejo por
  paridad. No hay sitios fijos.
- Episodios: 40 por corrida (20 *rodeo* y 20 *atajo*, balanceados por construcción), con `d_ini = 4`,
  `max_pasos = 60` y `E_test = 0.3`, sin aprendizaje y sin boca.

**Mundo ESCALA (E, secundario):** 15 × 13, `cierre = 6`, `d_ini = 5`, las demás constantes iguales. El rodeo más
largo puede superar `H_M = 20` ondas; no se toca `H_M`.

**Brazos (11 × 20 semillas):**
- CIEGO, CAMINO (lectura del 21-sep), GRAD (sólo grad), FILTRO (sólo filtro) y **GF (el candidato)**.
- **BRÚJULA**: GF, pero el veneno recordado **no bloquea** la difusión.
- BARAJADO, INVERTIDO y PLACEBO (GF más 3 sorteos descartados).
- CIEGO_E y GF_E, en el mundo E.

**Anclas.** `construye_subida.py` (`a562a599f7c2bcda`) genera `mundo_subida.py` (`484e34db8f2150da`) por anclas con
conteo exacto desde `experimentos/nivel06_rodeo_obligado/mundo_muralla.py` (**sha fijado `6e515713c86d8bf4`**).
La cadena de orígenes es `mundo_2d` ← `mundo_mapa_rodeo` (`7ab34aed9acffaa0`) ← `mundo_mapa` ← `organismo_v13`
(`cc8b16b492d4d324`).
- Runner: `corre_subida.py` (`374846482660917d`). Verifica el sha del mundo al arrancar y compara las entradas
  **campo a campo** contra `corre_muralla.kw_de` (regla 14). Sólo difieren `alto`, `prueba.d_ini` y
  `prueba.cierre`, que son las declaradas aquí.
- Arnés: `identidad_subida.py` (`7cd52e371eeb79f0`).
- Análisis: `analiza_vuelta_toro.py` y `analiza_barajado.py`.

## 4. Puertas

Una línea por puerta. Los umbrales de R-1a a V1 son **los del 21-sep, sin tocar**; R-1c y E-1/E-2 son nuevas.

| # | puerta | medida (mediana de 20 semillas) | umbral | nulo declarado |
|---|---|---|---|---|
| R-1a | rodea | `limpio(rodeo)` de GF | ≥ 0.60 | CIEGO en rodeo de verdad: 0.006 (21-sep), 0.0 (humo) |
| R-1b | es el mapa | GF − max(CIEGO, BARAJADO) | ≥ 0.25 | 0 |
| **R-1c** | **es el veneno recordado** | GF − BRÚJULA | **≥ 0.25** | 0 (H0-BRÚJULA) |
| R-2a | no es huida | `huye(rodeo)` de GF | ≤ 0.20 | CIEGO 0.75–0.90 |
| R-2b | balanceada | J = limpio(rodeo) + limpio(atajo) − 1 | ≥ 0.50 | 0 |
| R-3 | cuesta menos | `pasos_cens` GF / CIEGO | ≤ 0.70 | 1.00 |
| R-4 | no regresión | comida GF / CIEGO | ≥ 0.90 | 1.00 |
| R-5 | muertes | GF / CIEGO | ≤ 1.25 | 1.00 |
| C1 | decisivo | `limpio(rodeo)` de INVERTIDO | ≤ 0.20 | — debe caer |
| PLACEBO | instrumento | \|GF − PLACEBO\| en R-1a | ≤ 0.15 | si no, la serie **no se lee** |
| V1 | validez | la comida y los 21 venenos en `M` de GF | 20/20 | regla 10 automática si ≥ 60 % |
| E-1 (sec.) | escala | `limpio(rodeo)` de GF_E | ≥ 0.60 | — |
| E-2 (sec.) | escala | GF_E − CIEGO_E | ≥ 0.25 | 0 |

**Nulo del margen (regla 15).** PLACEBO mide la dispersión del mismo brazo con otra trayectoria, y su tope (0.15)
queda por debajo de los márgenes 0.25 de R-1b y R-1c. **No calculé la n que pasa con probabilidad ≥ 0.95 bajo el
nulo:** no hay serie del nulo. Se declara no verificado.

Se reportan sin ser puerta: GRAD y FILTRO por separado (atribución), el pareado GF > BRÚJULA y GF > CIEGO (k/20) y
`analiza_barajado.py`.

## 5. Predicciones (con rango), firmadas después del humo de una semilla

- GF `limpio(rodeo)` **0.80–1.00** (punto 0.90). `limpio(atajo)` 0.75–1.00. J **0.60–0.95**. `huye` 0.00–0.10.
- **BRÚJULA** `limpio(rodeo)` **0.00–0.15** y `pisa(rodeo)` ≥ 0.80. R-1c pasa con un margen de 0.65–1.00.
- CIEGO 0.00–0.10. **CAMINO 0.00–0.25**: en un mundo partido de verdad, la lectura del 21-sep no rodea.
- **Puede fallar: ninguno de los dos ingredientes solo pasa R-1a.** GRAD solo 0.10–0.55; FILTRO solo 0.00–0.40. Si
  uno de ellos da ≥ 0.60, el mecanismo mínimo era más chico y lo digo.
- BARAJADO 0.00–0.40. **Riesgo:** con la lectura por signo, BARAJADO conserva el mapa en las semillas donde la
  permutación mantiene `v_A > 0` y `v_B < 0`; el 21-sep eso pasó en 8 de 20. Si pasa en ≥ 10/20, R-1b puede caer
  sin que el mecanismo esté mal (§6).
- INVERTIDO ≤ 0.10. PLACEBO dentro de ±0.10 de GF.
- R-3: razón 0.20–0.45. R-4: 1.5–4.0×. R-5: 0.2–0.7×. V1 ≥ 18/20 (riesgo: la muralla sin hueco queda del lado sin
  comida).
- **E-1: GF_E 0.40–0.90 (punto 0.65). Es la que más espero que caiga:** `H_M = 20` puede no cubrir el rodeo de
  15 × 13. E-2 pasa.

## 6. Controles que pueden ganarle al candidato y qué refuta

- **BRÚJULA** es el control que puede ganar. Si R-1c < 0.25, lo que rodea es saber dónde está la comida más el
  filtro, no el veneno recordado que corta el paso: **H refutada**.
- **GRAD solo o FILTRO solo ≥ 0.60** no refuta H, pero **refuta el mecanismo mínimo** (sobraría una pieza).
- **Refutan H además:** R-1a < 0.60, J < 0.50, C1 > 0.20 o `huye` > 0.20.
- **BARAJADO bajo lectura por signo** es un control parcial (declarado antes de correr): quita información sólo
  donde rompe el signo. `analiza_barajado.py` separa las dos clases de semilla. Si R-1b cae y BARAJADO sólo rodea en
  las semillas de signos conservados, se registra así y R-1b no se reinterpreta: cae por la letra.

## 7. Las cuatro trampas

1. **Canal simétrico:** no aplica.
2. **Acierto sin balancear:** hay *atajo* 20/20 y J (R-2b).
3. **Mundo que se come la comida:** `regen = 50`, y cada episodio restaura `objs`, `M`, `E` y la traza.
4. **Sitios fijos:** la geometría se sortea por semilla con un rng independiente, más espejo y origen. **Trampa
   quinta, nueva:** una muralla en un toro no parte el toro (§1). Con `cierre` sí lo parte, y en el humo CIEGO y
   CAMINO dan 0.0.

## 8. Semillas nuevas

**Serie 6601–6620; réplica 6621–6640; humo 6641; arnés 6642–6644.** Lo verifiqué con un script sobre todo el repo:
- rangos «a–b», «desde», «seed» y «semilla» en `.md`, `.py`, `.txt` y `.log`;
- listas `semillas` y `seeds` de todos los JSON;
- nombres `_sA-B` de archivos.

Resultado: **0 usos de 6601–6661.** Un `grep -w` crudo sí encuentra esos números dentro de JSON de datos, pero como
conteos y pesos, no como semillas.

## 9. Lo ya corrido y lo que cambió antes de la serie

- **Arnés `identidad_subida.py`: IDENTIDAD 42/42.**
  - 30 identidades bit a bit con las perillas apagadas: anillo v13, anillo con mapa, `modo='2d'`, `modo='rodeo'`, y
    muralla CIEGO / MAPA / CAMINO / placebo / barajar / invertir, en las semillas 6642–6644.
  - 12 controles que deben diferir: `cierre`, `grad`, `filtro` y `brujula`.
  - JSON: `datos/humo/identidad_subida_20260923_153614.json` (`16d15f6dcbfd2d8a`).
- **Depuración (semilla 6642, cinco corridas, no son dato).**
  - (a) Con el filtro sin condición, `valor(A)` quedaba en −0.226 desde el paso 6 000. Una comida que empieza mala
    quedaba filtrada para siempre y nunca se volvía a probar. **Arreglo antes del humo:** el filtro sólo actúa con
    meta recordada.
  - (b) GF en el mundo viejo dio `limpio` 1.0 en 4.4 pasos. Eso delató la vuelta del toro (§1) y llevó a `cierre`.
- **Humo:** `python experimentos/subida_n6/corre_subida.py --humo`, 6 corridas, T = 20 000, 30.4 s. JSON:
  `experimentos/subida_n6/datos/humo/subida_humo_20260923_153753.json` (`ce1249637262520a`).
  - GF: 0.95 / 0.90 (rodeo / atajo), `huye` 0.0, pasos 16.8.
  - BRÚJULA: 0.0 / 0.1, `pisa(rodeo)` 1.0.
  - CIEGO, CAMINO, BARAJADO e INVERTIDO: 0.0.
  - Comida GF / CIEGO: 365 / 113. V1: 21/21.
  - PLACEBO, GRAD, FILTRO y el mundo E no se corrieron (tope de 6).

## 10. Criterio y vocabulario (propuesta de puntos; decide el director)

- **FUNCIONA:** 11/11 principales en la serie **y** en la réplica, con la misma letra.
  - Propuesta: nivel 6 de **50 → 70 %**, y **75 %** si E-1 y E-2 también pasan en las dos.
  - Vocabulario: *«en un mundo 2D partido por veneno recordado con un solo cruce (geometría sorteada), el
    organismo llega a la comida recordada por el hueco sin pisar el veneno; si el veneno recordado no corta el
    campo, pisa la muralla»*.
  - **Prohibido:** «planifica» (no simula trayectorias; sube por un campo que se difunde por relajación entre
    vecinos, y el director decide si eso cuenta), «entiende el espacio», «rodea» sin el mundo al lado.
- **HAY ALGO MODESTO:** el núcleo (R-1a, R-1c, R-2b) pasa en serie y réplica pero cae otra principal. También cuenta
  una réplica que cae una puerta a una semilla del umbral, lo que dispara la regla 12. Propuesta: **55–60 %**.
- **NO:** el núcleo cae en la serie. Queda en 50 % y queda el ERR de §1.
- **Lo que falta para el 100 % aunque FUNCIONE:**
  - dos metas en 2D (elegir entre dos comidas en el mundo partido);
  - el port a v14.2 (el constructor sobre v14.2 no existe);
  - el mapa construido y corregido dentro del episodio (hueco que se mueve: desdecirse);
  - varios rodeos compuestos más allá de `H_M`.

## 11. Comandos (los corre el coordinador; un Pool ≤ 6)

```
python experimentos/subida_n6/identidad_subida.py
python experimentos/subida_n6/corre_subida.py --desde 6601 --n 20 --pool 6     # serie, 220 corridas
python experimentos/subida_n6/corre_subida.py --desde 6621 --n 20 --pool 6     # réplica (siempre)
python experimentos/subida_n6/corre_subida.py --lee experimentos/subida_n6/datos/<tag>.json --sello <sha16>
python experimentos/subida_n6/analiza_barajado.py experimentos/subida_n6/datos/<tag>.json <sha16>
```

Costo estimado, medido en el humo: ~5 s por corrida de T = 20 000, o sea ~25 s a T = 100 000 en P y ~35 s en E
(estimado, E no se midió).
- Serie: 180 × 25 + 40 × 35 ≈ **5 900 s de CPU (1.6 h)**, **≈ 17 min de pared con Pool 6**.
- Réplica: igual.
