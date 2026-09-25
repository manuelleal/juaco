# EXPLORATORIO, no es dato

# HALLAZGOS — comité 2, EXPLORADOR FABLE 1: PUENTEO DIAGNÓSTICO V143 ⟷ O1 (25-sep-2026, 15:30–16:25; la serie sigue corriendo sola)

**Misión:** llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).

**Estado al escribir esto: PARCIAL.** El instrumento está construido y verificado (arnés 16/16). La serie (5 puentes solos × semillas
36001–36010, un proceso por corrida, máximo 4 a la vez) está corriendo desde las 15:54; cada corrida tarda 390–560 s porque otros agentes
ocupan el PC. Al cierre de este texto sólo está completa la semilla 36001. **Las tablas de abajo se regeneran con `python lee_puenteo.py`
cuando haya más JSON en `datos/`**; el lanzador encadenado seguirá solo con: control `v143p` s36001 y después los pares
`patas_bmala` y `patas_bbuena` en 36001–36005 (marcadores `_omitido` en 36006–36010 para que las salte).

**Veredicto provisional (UNA semilla; no es dato): HAY ALGO.** En s36001 (V143 0.722, O1 0.933):
- **PATAS de O1 solas → 0.960** (8/9 establecidos) y **BOCA de O1 entera → 0.963**: cada una, sola, cierra la brecha completa en esa semilla.
- **BOCA_BUENA sola → 0.900** (8/9 establecidos): la mitad de la boca —no morder lo bueno de sobra, probar lo desconocido sólo con cuerpo— recupera el 84 %.
- **BOCA_MALA sola (la limpieza de O1) → 0.210** y **MEMORIA (tabla de O1 por la vía lenta) → 0.123**: HUNDEN. La regla de limpiar y la tabla
  de O1 sólo sirven encima del cuerpo que las acompaña; trasplantadas solas, matan.

## 1. Qué es el instrumento (`comite2/puenteo/`, sólo copias; nada fuera de la carpeta)
- `carros/V143P.py`: copia de `V143.py` (2a03048a7f1525e5) con `actua()` partido en `actua_patas` (objetivo + motor, consume `rng.normal`),
  `actua_boca` (progreso + decisión de morder, consume `rng.random`) y `actua_cierra` (efectos de la decisión FINAL: memoria de rechazo,
  telemetría del filtro, y la acción que aprende la opción APR es la EJECUTADA). Compuestas, son V143 línea por línea.
- `carros/O1P.py`: copia de `O1.py` (99436afa2715f028) con `actua()` partido en `decide()` (blanco, mov, modo limpieza) y `boca(k, lev, limpia)`.
- `carros/HIB.py`: aloja los dos cerebros viviendo la misma vida (mismo obs, `resultado`, `muere`, `nace`, `al_parir` con memoria doble).
  V143 decide todo salvo las piezas puenteadas: `patas` (mov de O1; el motor de V143 corre igual y consume su rng), `boca_buena` (letra que
  O1 no sabe mala: O1 decide), `boca_mala` (letra que O1 sabe mala: O1 decide = sólo limpieza costeable), `memoria` (el nacido no lee el nodo;
  recibe la tabla de O1 por la MISMA vía lenta, R = +1/−3/0 por signo, 5 repeticiones por lección). O1 NO consume el rng del cuerpo.
- **Arnés `arnes_puenteo.py` (N 9, s 36901, T 2000, fundador limpio): 16/16.** V143P == V143 salida ENTERA; O1P == O1 salida ENTERA;
  HIB todo en 0 == V143 en todo salvo `d['carro']` (física, `_carrera`, rng del mundo); HIB patas+boca_buena+boca_mala == O1 en todo salvo
  `d['carro']` y `exp_hasta`; cada puente solo cambia la física y es determinista.
- `corre_puenteo.py` (una corrida = `pista.run` con los argumentos de `corre_v143.tarea` + `juez.resumen_linaje`; JSON antes de nada),
  `lanza.py` (cola, máximo 4 procesos, sin Pool, salta lo ya corrido), `lee_puenteo.py` (tablas).
- Bases V143 y O1 por semilla: los crudos de la serie `frio_carrera` de hoy (misma pista, mismos shas, mismos mundos, T 100 000, fundador limpio).
  El control `v143p` (HIB sin puentear a T completo) queda en la cola para confirmar que reproduce `v143_s36001.json` (P9).

## 2. Tabla por puente — mediana sobre semillas; pareado con la MISMA semilla (`python lee_puenteo.py` la regenera)
Camino recuperado = (puente − V143)/(O1 − V143). Vida hijo = mediana de las vidas de los cuerpos NO fundadores muertos. **Sólo s36001 al escribir.**

| puente | sem | R0 real med | camino recuperado | gana a V143 | dif vs V143 | establecidos/9 | R0 de establecidos | vida hijo | vida fund | hijo sin parir | hijos/hijo | B+D/linaje | causas h/s/v/s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v143 (base) | 1 | **0.722** | – | – | – | 6 | 0.901 | 1474 | 46 | 0.42 | 2.33 | 551 | 56/60/837/942 |
| **patas** | 1 | **0.960** | +113 % | 1/1 | +0.238 | 8 | 0.963 | 1530 | 34 | 0.42 | 2.33 | 484 | 39/24/620/625 |
| **boca** (buena+mala) | 1 | **0.963** | +114 % | 1/1 | +0.241 | 6 | 0.965 | 1817 | 200 | 0.50 | 1.20 | 174 | 115/124/270/294 |
| **boca_buena** | 1 | **0.900** | +84 % | 1/1 | +0.178 | 8 | 0.931 | 1708 | 48 | 0.44 | 2.23 | 243 | 80/60/471/486 |
| boca_mala (limpieza) | 1 | **0.210** | −242 % | 0/1 | −0.512 | 2 | 0.903 | 1401 | 200 | 0.63 | 0.74 | 299 | 126/154/430/176 |
| memoria (tabla O1 → vía lenta) | 1 | **0.123** | −284 % | 0/1 | −0.599 | 2 | 0.908 | 600 | 49 | 0.92 | 0.69 | 702 | 131/153/1060/1154 |
| o1 (techo) | 1 | **0.933** | – | 1/1 | +0.211 | 7 | 0.933 | 4182 | 200 | 0.28 | 3.42 | 354 | 40/40/292/268 |
| patas_bmala, patas_bbuena | 0 | (en cola, 36001–36005) | | | | | | | | | | | |

Por semilla (R0 · establecidos · vida hijo): 36001 — v143 0.722·6·1474 · patas 0.960·8·1530 · boca 0.963·6·1817 · boca_mala 0.210·2·1401 ·
boca_buena 0.900·8·1708 · memoria 0.123·2·600 · o1 0.933·7·4182. Las demás semillas: `lee_puenteo.py`.

Telemetría del híbrido (no puntúa; última instancia por linaje): O1 y V143 discrepan en el **mov ~50–66 % de los pasos** y en la boca
**13–48 % de las decisiones**; con `patas`, la discrepancia de boca sube a 48 % (63 351/132 205 en letras malas) porque el cuerpo de V143
llega a lo malo mucho menos y la boca de V143 igual quiere morderlo.

## 3. Dónde está la brecha (lectura de una semilla, a confirmar)
1. **No está en la memoria ni en la limpieza.** Darle al nacido la tabla exacta de O1 lo hunde (0.12); darle la regla de limpiar de O1 lo hunde
   (0.21). Coincide con trasplantes (ENSEÑA inerte; `nomalo` 0.18): el hijo de V143 no muere de ignorancia.
2. **Está en las DOS decisiones de acción, y cada una basta:** a qué objeto ir (patas) y si morder lo que hay bajo el cuerpo (boca), y de la
   boca, sobre todo la parte "buena": **no morder lo bueno cuando no hace falta, y probar lo desconocido sólo con reserva**.
3. **El mecanismo, visible en la física de `boca_buena`:** mordidas buenas 7002 → 4397 → queda más comida y agua en el mundo (A 1.6 → 2.0 por
   paso) → el FILTRO de V143 tiene meta más veces → mordidas malas 4959 → 2189 → muertes por veneno/sal 1779 → 957 → 8/9 linajes establecidos.
   Con `patas`: el cuerpo va a lo que le sirve en vez de a lo más cercano → llega menos a B/D → B+D 551 → 484 y veneno+sal 1779 → 1245.
   Las dos piezas convergen en lo mismo: **el cuerpo de V143 se pone encima de lo malo demasiadas veces** (por ir a lo más cercano y por
   vaciar lo bueno de su alrededor), y la boca de FABRICA, con hambre, lo muerde aunque el linaje sepa que es malo.

## 4. Traducción: qué capacidad le falta al bicho, como mecanismo local (SIN copiar la regla de O1)
- **Saciedad que frene la boca sobre lo bueno.** Hoy la boca de FABRICA suma `HAMBRE_BOCA·hambre + 0.5` y muerde lo bueno casi siempre (el 0.5
  es un sesgo a morder aun sin hambre). Falta una señal local del propio cuerpo —"esta necesidad ya está por encima del umbral de parto"—
  que reste al logit de la boca en proporción a lo lleno. Es una regla local: sólo lee E y Ag propios, ya los tiene. En trasplantes, `sac2/sac6`
  (reserva −2/−6) no movieron nada: la dosis era chica frente a un logit de escala Vb/0.3 (≈ +4 a +7); O1 la hace absoluta (MARGEN).
- **Neofobia con reserva.** Probar una letra desconocida sólo si min(E, Ag) deja margen para el golpe (O1: PRUEBA 0.5). Mecanismo local: la
  boca sobre un código NO familiar (`_fam` False, valor lento ≈ 0) exige más reserva que sobre uno familiar. El cuerpo ya sabe si el código es
  familiar (puerta_pat): sólo falta que esa señal pese en la boca.
- **Patas que lean el valor, no la distancia.** `_see` elige el objeto más cercano y el FILTRO sólo excluye lo malo cuando hay meta. Falta
  que el blanco sea el que maximiza valor propio/(distancia), con la fila activa. Es la señal que ya calcula la boca (`_vnec`), llevada a las
  patas; en trasplantes el cable lineal (+2) dio +0.13 sin dosis-respuesta, aquí el blanco entero de O1 dio +0.24 en s36001.
- Lo que NO hay que darle: ni la tabla de valencias (la que tiene basta), ni una regla de limpieza (la suya, APR, ya está y trasplantada
  la de O1 mata).

## 5. Predicciones (`PREDICCIONES_previas.md`, firmadas 16:05) frente a s36001
P1 patas el mejor en [0.75, 0.85]: **refutada por arriba** (0.960). P2 boca_mala ≈ V143: **refutada** (hunde −0.51). P3 boca_buena no sube:
**refutada** (+0.178). P4 boca < patas: empate (0.963 vs 0.960). P5 memoria ≈ V143: **refutada** (hunde −0.60). P6 ningún puente ≥ 0.90:
**refutada** (tres lo superan). P8 patas sube establecimiento: se cumple (6 → 8). P7 y P9: pendientes (en cola).
Firmé mirando trasplantes (cables lineales chicos) y me equivoqué en el sentido: la política entera de una pieza pesa mucho más que un cable.

## 6. Qué falta y contrato
- Semillas 36002–36010 de los cinco puentes solos (~80 min más de cola), control `v143p` s36001, pares en 36001–36005. Todo cae en `datos/`;
  `python lee_puenteo.py` rehace las tablas; **borrar al cierre los marcadores `_omitido`** (`patas_b*_s36006–36010.json`).
- Sin git, sin Pool, sin matar procesos, nada fuera de `comite2/puenteo/`, ni `eval` ni `exec` (los carros se cargan con importlib).
- Declarado: con `patas` el motor de V143 aprende con su propio `m` aunque el cuerpo se mueva con el mov de O1; con `boca` la opción APR aprende
  sobre la acción ejecutada. `MEM_REPS = 5` es arbitrario. Los pares `patas_boca` y `todo` no se corren: son O1 en la física (arnés (4)).
