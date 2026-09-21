# PREREGISTRO — NIVEL 6, BLOQUE "RODEO OBLIGADO": un mundo 2D donde alejarse no sirve

**21 sep 2026. Creador (Opus). Escrito ANTES de la serie. No se ha corrido ninguna serie: sólo el arnés de
identidad (21/21) y dos humos de un proceso (§9), cuyos números NO se interpretan y cuyo único papel es decidir
los dos parámetros de instrumento de §3 y declarar los dos defectos de instrumento de §10.**

Antecedente que este bloque continúa: `experimentos/nivel6_2d/` (REGISTRO L3942): *con el veneno recordado entre
él y la comida **no rodea: se aleja**; el mecanismo distingue el flanco barato y no lo usa* (R1 = 0.000 con mapa
contra 0.525 sin mapa; rodeo falso 0.05). Diagnóstico literal del registro: **«en 2D el sesgo de `M` es un voto
global y el veneno no repele el camino, repele el acercamiento»**. El registro dejó escrito: *rediseñar el mundo
antes de replicar*.

---

## 1. Hipótesis

**H.** En un mundo donde **alejarse no sirve** (el toro está partido en dos por una muralla de veneno recordado
con un solo hueco, y el episodio tiene presupuesto de pasos), la **misma tabla `M`** leída como **campo de valor
difundido por el espacio libre** — el veneno recordado **bloquea el camino** en vez de repeler el acercamiento —
lleva al organismo hasta la comida recordada **sin pisar el veneno**, por encima de CIEGO y de MAPA_BARAJADO;
y no lo hace huyendo (se mide y se penaliza), ni pagando más pasos que el azar.

**H0 (lo que el registro ya midió y aquí se replica como brazo):** la lectura actual (`MAPA`, voto global
descontado) no rodea; se aleja.

## 2. Mecanismo mínimo y memoria nueva

**Memoria nueva persistente: CERO.** La tabla `M` (posición → último patrón visto) ya existe desde `nivel6_mapa`.
Lo único nuevo es **cómo se lee**:

```
U[c] = valor(M[c])                      para cada comida recordada (fuente)
U[p] = valor(M[p]) y NO propaga         para cada veneno recordado (bloquea)
U[n] = max(U[n], disc_M * U[q])         relajación local entre vecinos, H_M ondas
sesgo(a) = gamma_M * U[vecino en la dirección a]
```

Es una **relajación local entre celdas vecinas** (frente de onda), sin retropropagación, con las **mismas**
constantes ya existentes (`gamma_M`, `disc_M`, `H_M`) y la **misma** `valor()`. `U` es un **array derivado**: se
invalida cuando `M` cambia o cuando morder cambia `valor()`, y se recalcula; no se guarda entre corridas ni entra
al organismo. Coste declarado: O(H_M · L · 4) por recálculo (≈ 3 500 relajaciones en la rejilla 11×9), unas
1 000 veces en 100 000 pasos. **El organismo (v13 dentro de `mundo_2d`) no cambia: ni `valor()`, ni la boca, ni
el aprendizaje.** Perilla `camino`; con `camino=0` es `mundo_2d` bit a bit.

## 3. Mundo (el que OBLIGA) e instrumento

Rejilla **toroidal 11 × 9** (99 celdas), 4 direcciones, `r_vis = 1`, `regen = 50`, `T = 100 000`.
**Muralla:** la **fila completa** (11 celdas) **menos un hueco** → 10 sitios de veneno; el toro queda partido en
dos mitades y el hueco es **el único cruce**. **Una** comida al otro lado. Alejarse no abre ningún camino.

**Trampa «sitios fijos que se memorizan» (LA trampa aquí): la geometría se sortea POR SEMILLA** con un rng
independiente (`default_rng(1000003·seed+7)`, no toca el rng del organismo): columna del hueco `gx`, columna `fx`
y fila `fy` de la comida, con `|fx − gx| ≥ 2`; además el origen `_F0` es azaroso y el mapa se refleja por paridad
de semilla. Ningún sitio coincide entre semillas: memorizar no sirve.

**Episodios** (40 por corrida, sin aprendizaje y sin boca, `E_test = 0.3`, `max_pasos = 60`), dos casos alternados
y **balanceados por construcción** (misma muralla, misma comida; sólo cambia la columna de salida):

| caso | salida | el camino recto… | qué hace bien un organismo que rodea |
|---|---|---|---|
| **rodeo** (20) | columna `fx`, a `d_ini = 5` de la muralla por el lado contrario | cruza **veneno** | desviarse hasta el hueco, cruzar y volver |
| **atajo** (20) | columna `gx` (la del hueco), a `d_ini = 5` | cruza el **hueco** (limpio) | ir **recto** |

Una política «siempre recto» falla *rodeo*; una política «siempre desviarse» falla *atajo*. Por eso la tasa se
reporta **balanceada** (regla 15 de EQUIPO / criterio v3 §2.5).

**Brazos (6):** `CIEGO` (sin mapa) · `MAPA` (lectura H1, la refutada) · `CAMINO` (la candidata) · `BARAJADO`
(CAMINO con el valor permutado entre celdas y entre píxeles: mismo empuje, sin información) · `INVERTIDO`
(CAMINO con el signo del valor cambiado: control decisivo) · `PLACEBO` (CAMINO + 3 sorteos por decisión
descartados: misma ley, otra trayectoria; criterio v3 §2.4).

**Anclas.** `construye_muralla.py` genera `mundo_muralla.py` **por anclas con conteo exacto** desde
`experimentos/nivel6_2d/mundo_2d.py` (**sha fijado `24da4ab1644eb92a`**, verificado en la construcción), que a su
vez viene de `mundo_mapa_rodeo` (`7ab34aed9acffaa0`) ← `mundo_mapa` (`207d6a1954336b18`) ← `organismo_v13`
(`cc8b16b492d4d324`). `mundo_muralla.py` = `6e515713c86d8bf4`. Arnés `identidad_muralla.py`: **21/21** (§9).

## 4. Puertas (una línea por puerta, umbral al lado; ninguna en el nulo)

| # | puerta | medida | umbral | nulo declarado |
|---|---|---|---|---|
| **R-1a** | **rodea** | mediana de `limpio` en *rodeo* (llega a la comida con `pisa == 0`) de CAMINO | **≥ 0.60** | CIEGO ≈ 0.15 (medido en el humo); 0.60 está a +0.45 del nulo |
| **R-1b** | **y es el mapa** | `limpio(CAMINO) − max(limpio(CIEGO), limpio(BARAJADO))` | **≥ 0.25** | 0 |
| **R-2a** | **no es huida** | mediana de `huye` en *rodeo* (no come y se alejó ≥ 2 de la comida) | **≤ 0.20** | CIEGO ≈ 0.80 |
| **R-2b** | **balanceada** | `J = limpio(rodeo) + limpio(atajo) − 1` de CAMINO (ver ERR candidato, §10) | **≥ 0.50** | 0 |
| **R-3** | **cuesta menos** | mediana de `pasos_cens` (pasos, censurados a 60 si no llega limpio) CAMINO / CIEGO | **≤ 0.70** | 1.00 |
| **R-4** | **no regresión** | comida total en el mundo muralla, CAMINO / CIEGO | **≥ 0.90** | 1.00 |
| **R-5** | **muertes** | muertes en 100 000 pasos, CAMINO / CIEGO | **≤ 1.25** | 1.00 |
| **C1** | **decisivo** | `limpio(rodeo)` de INVERTIDO | **≤ 0.20** | — debe fallar |
| **PLACEBO** | **el instrumento** | PLACEBO debe dar lo mismo que CAMINO dentro de ±0.15 en R-1a | — | si no, la serie no se lee |
| **V1** | **validez** | la comida y las **10** celdas de la muralla en `M` | **20/20** | regla 10 si cae y ≥ 60 % la cumplen |

**No regresión del tronco (aparte):** con `camino=0, placebo=0` y sin `modo='muralla'`, `mundo_muralla` ≡
`mundo_2d` ≡ `mundo_mapa` ≡ `organismo_v13` **bit a bit** (arnés, §9). El órgano es **de experimento, no del
tronco**: no se propone a v15.

## 5. Predicción numérica (con rango), firmada

- **R-1a:** `limpio(rodeo)` de CAMINO **0.60–0.85** (punto 0.70). CIEGO **0.05–0.25**; MAPA **0.05–0.30**
  (predigo que **MAPA no rodea**, replicando nivel6_2d); BARAJADO **0.10–0.40**.
- **R-2a:** `huye(rodeo)` CAMINO **0.05–0.20**; CIEGO **0.60–0.90**.
- **R-2b:** `J` **0.50–0.75**.
- **R-3:** razón de pasos **0.55–0.75**.
- **R-4:** **1.2–2.5×** (predigo que el órgano **ayuda** a comer en su mundo, no sólo que no estorba).
- **R-5:** **0.5–0.9×**.
- **C1:** INVERTIDO `limpio(rodeo)` **≤ 0.10** y `pisa(rodeo)` **≥ 0.80**.

## 6. Control que puede fallar, y qué refuta

- **BARAJADO** es el control que puede fallar y el que más me preocupa: si `limpio(CAMINO) − limpio(BARAJADO)
  < 0.25`, lo que el campo aporta es **geometría de bloqueo, no el contenido del mapa**, y la hipótesis queda
  **refutada** (sería «el organismo rodea porque el campo lo empuja, no porque recuerde qué hay ahí»).
- **Refutan H además:** R-1a < 0.60; o `huye` > 0.20 (rodea huyendo); o `J` < 0.50 (siempre se desvía); o
  R-3 > 0.70 (rodea pero no le sale a cuenta); o PLACEBO fuera de ±0.15 de CAMINO (la puerta está rota y la
  serie **no se lee**).
- **Vocabulario si pasa:** *«con el veneno recordado entre el cuerpo y la comida y sin escapatoria, la misma
  tabla leída como campo bloqueado llega a la comida sin pisar el veneno»*. **No** se dirá «planifica».

## 7. Las cuatro trampas

1. **Canal simétrico:** no aplica (no hay canal social).
2. **Acierto sin balancear:** cubierto por el caso *atajo* y por `J = p1 + c1 − 1` (R-2b).
3. **Mundo que se come la comida:** la comida regenera en su sitio (`regen = 50`) y los episodios restauran
   `objs`, `M`, `E` y la traza antes de cada uno; el muestreo de *rodeo* y *atajo* es 20/20 por construcción.
4. **Sitios fijos que se memorizan (LA trampa aquí):** geometría **sorteada por semilla** con rng independiente
   + origen azaroso + espejo por paridad (§3). CIEGO no puede saber dónde está el hueco.

## 8. Semillas NUEVAS (verificadas libres con grep en `registro/`, `experimentos/`, `datos/`)

**Serie: 1701–1720. Réplica: 1721–1740.** (Tomadas y evitadas: 1541–1660, 2101–2360.)
Los humos de §9 usaron **1701**; si el coordinador lo considera contaminado, la serie corre **1702–1721** y la
réplica **1722–1741**.

## 9. Arnés e instrumento — lo ya corrido (un proceso, sin Pool)

`python experimentos/nivel06_rodeo_obligado/identidad_muralla.py` → **IDENTIDAD 21/21**: 12 identidades bit a bit
(anillo v13 sin mapa; anillo con mapa; rejilla `modo='2d'`; anillo `modo='rodeo'`; semillas 1701–1703) y 9
controles que **DEBEN DIFERIR** (camino=1 difiere; placebo=3 difiere; muralla H1 ≠ CAMINO), los 9 difieren.

Humos (`--humo`: 1 semilla, T = 20 000, ≤ 6 corridas, **escriben su JSON**): `datos/humo/muralla_humo_20260921_170208.json`
(`cad376dffbf3604d`, 6 brazos, `r_vis=2`, `d_ini=3`) y `datos/humo/muralla_humo_20260921_170342.json`
(`8893c69e31ccb2eb`, 4 brazos, `r_vis=1`, `d_ini=5`) y el definitivo con los valores de §3 y las puertas de §4
`datos/humo/muralla_humo_20260921_170544.json` (`4fea72d96bb85e0f`, 5 brazos, 5 corridas, 6/10 puertas — **no se
interpreta**: una semilla). En ese humo **la puerta PLACEBO pasa** (|CAMINO − PLACEBO| = 0.05) y **C1 se comporta
como control decisivo** (INVERTIDO `pisa(rodeo)` 0.80 contra 0.50 de CAMINO).

## 10. Lo que el humo cambió ANTES de la serie, y dos defectos declarados

**(a) `r_vis` y `d_ini` (instrumento, no umbral).** Con `r_vis = 2` y `d_ini = 3` la retina **nunca** queda vacía
cerca de la muralla (10 objetos en una fila de 11), el sesgo de `M` no llega a actuar y **los seis brazos dan lo
mismo** (`limpio(rodeo)` 0.0 en CAMINO, BARAJADO, INVERTIDO y PLACEBO). El mundo no deja hablar al órgano. Con
`r_vis = 1` y `d_ini = 5` el órgano sí actúa (CAMINO 0.45 / CIEGO 0.15 / MAPA 0.20; `huye` 0.10 / 0.80 / 0.55;
pasos 38.8 / 54.3 / 50.7). **Los valores de §3 son `r_vis = 1`, `d_ini = 5`**, fijados aquí, antes de la serie.

**(b) Candidato a ERR — `recto` está mal definido como control balanceado.** Escribí `recto = llega limpio en
≤ d0 + 2 pasos`; con `d0 ≈ 6–9` y la política ruidosa da **0.000 en todos los brazos**, incluido el que va recto:
mide el ruido de las patas, no la elección. **R-2b usa `limpio(atajo)`**, no `recto`; `recto` se **reporta** y no
es puerta. (Si el coordinador prefiere, esto se numera como ERR y se cita aquí.)

**(c) Riesgo abierto, dicho antes de correr:** en el humo de una semilla `limpio(rodeo)` de BARAJADO **empató**
con CAMINO (0.45 contra 0.45) y en *atajo* lo **superó** (0.55 contra 0.25). Una semilla no decide nada, pero
**R-1b es la puerta que espero que decida este bloque**, y hoy no tengo evidencia de que la pase. Mi predicción
de §5 (BARAJADO 0.10–0.40) es la que puede caer primero.

## 11. Comando exacto de la serie (lo corre el coordinador, un Pool a la vez)

```
python experimentos/nivel06_rodeo_obligado/corre_muralla.py --desde 1701 --n 20 --pool 6
python experimentos/nivel06_rodeo_obligado/corre_muralla.py --desde 1721 --n 20 --pool 6    # réplica
```
(120 corridas por serie: 6 brazos × 20 semillas, T = 100 000. Lectura del JSON con sello exacto:
`--lee datos/<tag>.json --sello <sha16>`.)

## 12. Pendiente declarado que NO pude verificar

**El organismo de este mundo es v13, no v14.2.** Toda la línea del mapa está anclada en `organismo_v13`
(`mundo_mapa` ← v13), y `organismo_v142.run` tiene la retina y las acciones del **anillo** cableadas
(`Wl = rng.uniform(.1,.4,(2,9))`): llevarla a la rejilla 2D exige rehacer `construye_mapa` → `construye_2d` sobre
v14.2, que es un bloque de construcción aparte con su propio arnés. Lo dejo declarado: **este bloque mide el
órgano sobre v13**, todas las comparaciones son internas (CAMINO contra CIEGO/MAPA/BARAJADO con **el mismo**
organismo), y por eso R-4/R-5 comparan dentro del mundo muralla y no contra el tronco. El port a v14.2 queda
como `construye_muralla_v142.py`, no escrito.
