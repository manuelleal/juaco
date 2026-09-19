# PREREGISTRO — LA ESCALERA DE NIVELES CON ALMA (nivel 13, BLOQUE ALMA · diseño de la escalera)

**MISIÓN (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales que
aprende, sobrevive, se comunica y se reproduce; con evidencia preregistrada. Este documento no persigue
"células, dinosaurios y sapiens" como biología: persigue **subir la escalera de niveles del proyecto (brief +
`registro/HANDOFF.md` §13, actualizada con los resultados del día 7) con nuestro propio protocolo**, y ver si
un alma que cura tras cada muerte con un menú CERRADO de parches locales la sube más rápido, igual, o nada,
frente a una curita al azar y frente a no curar. El objetivo final del proyecto es **llegar al nivel 10 y
superarlo (nivel 11)** por este camino.

**Corrección aplicada (director, antes de cerrar):** las "eras" NO son una escalera biológica; SON los niveles
que el propio proyecto ya trae preregistrados, empezando donde estamos realmente (nivel 5), no desde cero.

**Rol de este documento:** Diseñador de preregistros (tabla de roles de `registro/EQUIPO.md`) — redacta el
preregistro y el constructor por anclas; **no corre `Pool`**; entrega instrumento + runner + humo de un proceso.

**Frontera con el BLOQUE ALMA:** otro creador construye ahora mismo la base del bloque ALMA en
`experimentos/nivel13_alma/` (bucle muerte → curita → renace/hijo, nodo central de mensajes, interfaz de
archivos `alma_pregunta_<n>.json` / `alma_respuesta_<n>.json`, controles alma aleatoria y alma ninguna). **No se
tocan sus archivos.** A la fecha de este preregistro sólo existe `experimentos/nivel13_alma/MENU_curitas.md`
(el menú cerrado de 6 curitas para el mundo H-1/nivel 9, ya escrito por ese creador — se **hereda tal cual** en
la §3 de este documento, sin reabrirlo). El bucle genérico (`alma_pregunta_<n>.json`/`alma_respuesta_<n>.json`,
el nodo central) **todavía no existe como módulo importable**; `corre_eras.py` escribe **contra esa interfaz
descrita en el encargo** y trae su propio bucle mínimo compatible (mismo formato de archivo) para poder correr
el humo hoy. Cuando el módulo del otro creador exista, `corre_eras.py` se apunta a él por import y este bucle
propio queda como *fallback* documentado, nunca como sustituto silencioso.

---

## 0. Qué escalera es esta (HANDOFF §13 + cierre del día 7, no biología)

| nivel | nombre en el proyecto | instrumento que ya existe | qué falta hoy |
|---|---|---|---|
| **5** | comunicación con referencia | `experimentos/nivel12_mundo_familias/organismo_familias_b6.py` (canal + `k_ganadoras`) | nada: instrumento y letra ya corridos (bloques 4b/5) |
| **6** | planificación (mapa, dos metas) | `experimentos/nivel6_mapa/…` y el mundo de rodeo del día 7 (`nivel6_rodeo`) | nada: letra ya corrida y replicada |
| **7** | composición de ≥ 3 órganos | `experimentos/nivel7_3T_k/mundo_temporal_k*.py` | nada para k ≤ 3; k > 3 sin medir |
| **8** | aprendizaje abierto (desaprende lo que evita, sorpresa que acelera) | `organismo_familias_b3`/`v15f` (desaprende) + `nivel9_allostasis` (sorpresa) | **nunca se juntaron en un mismo brazo**; la sorpresa que acelera está REFUTADA sola (bloque 6, día 7) |
| **9** | vida (muerte real, linaje que se sostiene) | `experimentos/nivel11_mundo_vivo/organismo_vivo_h1.py` | **REFUTADO sin alma** (H-1, ver §1): R₀ 0.14–0.17, no 0.90 |
| **10** | población que aprende de mensajes y hereda | ninguno: exige juntar canal (b6/nivel5) + herencia por muerte (h1/nivel9) en el MISMO organismo | **el instrumento no existe**; se necesita un creador |
| **11 (superar la escalera)** | invención de una señal arbitraria no dada por el mundo, y su uso | ninguno | **el instrumento no existe**; ninguna perilla actual permite "inventar un token"; el alma no puede curar lo que no es una perilla (regla del menú cerrado) |

Este preregistro corre lo que hay (niveles 5–9 con sus instrumentos actuales) bajo el bucle alma/curita, y deja
escrito, sin inventar mecanismo nuevo hoy, por qué 10 y 11 están bloqueados por **falta de instrumento**, no por
falta de alma — eso mismo es una predicción falsable (§4).

## 1. El hecho que ya tenemos y que este preregistro NO vuelve a medir sin alma

`registro/REGISTRO_etapas_1_2.md`, entrada **H-1 — QUE LA MUERTE MATE** (18 sep 19:24 y réplica 19:28, semillas
701–740, 20 brazos × 20, REPLICADO): con muerte real que borra la memoria del individuo, el linaje **no se
reemplaza** — R₀ cae de 0.87–0.98 (control inmortal) a **0.14–0.17 en los CUATRO modos de herencia** ya
probados (nada, M1/valores, M1+pares/valores+tabla, barajado). ERR-62, cláusula de cierre escrita antes de
correr: *"ESTE MUNDO NO SOSTIENE LINAJES MORTALES con ninguna herencia ni con las rampas de dote, umbral,
objetos o coste."* Esas rampas (dote, umbral) y esa herencia (M1) **son literalmente curitas (c), (d) y (e) del
menú de `MENU_curitas.md`, ya intentadas sin alma, una a la vez, y las cuatro fallaron por igual.**

Esto fija la predicción central de este documento (§4): si el alma sube R₀ ≥ 0.90 en el nivel 9 combinando esas
mismas perillas EN SECUENCIA y CONDICIONADAS al historial del linaje (lo que ninguna corrida de H-1 probó: H-1
fijó la herencia para TODO el run, el alma la elige muerte a muerte), eso sería el primer resultado del
proyecto que contradice ERR-62 — y sería la evidencia más fuerte de todo el bloque ALMA. Si no la sube, ERR-62
queda confirmado con una búsqueda mucho más rica que la que lo escribió, y el nivel 9 se declara **cuello
estructural del mundo**, no de la herencia.

## 2. Qué es "una muerte" en cada nivel (para que el bucle alma tenga sentido en los cinco)

Sólo el instrumento del nivel 9 (`organismo_vivo_h1.py`, con `muerte_real=1`) tiene una muerte real dentro de
una sola corrida (el linaje entero vive y muere dentro de un `run()` de T=100 000 pasos). Los instrumentos de
los niveles 5–8 (`organismo_familias_b6.py`, `mundo_temporal_k*.py`, mapa) son **de una sola vida por semilla**:
corren T pasos y terminan, sin mortalidad interna. Para poder aplicar "una curita por muerte" en 5–8 sin tocar
esos instrumentos (regla dura: no editar archivos existentes), este preregistro define, EXPLÍCITAMENT Y COMO
SIMPLIFICACIÓN DECLARADA:

> **"Muerte" en los niveles 5, 6, 7 y 8 = el final de una vida (una corrida de una semilla hasta T o hasta el
> criterio de fallo de ese mundo, lo que llegue primero).** El alma cura **entre vidas**, no dentro de una vida:
> elige una entrada del menú de ese nivel (§3) que se aplica como argumento de la SIGUIENTE llamada a `run()`
> con la semilla siguiente. No hay nodo central compartido salvo el que el bucle propio de `corre_eras.py`
> simula por archivo (un JSON acumulador por nivel, sección "Frontera con el BLOQUE ALMA").

Esto es honesto pero limitado: en 5–8 el alma no está "reencarnando" al mismo linaje, está **recalibrando la
población de próximas vidas** con lo que aprendió de la anterior — un régimen más débil que el de nivel 9, y se
declara así en el reporte (§7, tres líneas honestas) para no inflar vocabulario (regla 6 de `EQUIPO.md`).

## 3. Menú cerrado de curitas, por nivel

### Nivel 9 (vida) — **se hereda tal cual `experimentos/nivel13_alma/MENU_curitas.md`, sin reabrirlo**
Las seis entradas (a) CONECTAR AL NODO, (b) SUBIR EL MIEDO, (c) DOTE MAYOR, (d) BAJAR EL UMBRAL,
(e) HEREDAR VALORES, (f) NADA — con sus invariantes y su cláusula del buscador, íntegras. Es el menú del
creador del bloque ALMA para `organismo_vivo_h1.py`; este documento no cambia una coma.

### Nivel 5 (comunicación con referencia) — instrumento `organismo_familias_b6.py`
Perillas ya existentes en ese archivo, ninguna nueva:

| id | nombre | qué toca | reversible |
|---|---|---|---|
| a | SUBIR GANADORAS | `k_ganadoras ← min(k_ganadoras+1, 3)` (perilla ya medida en bloque 5; sube cuántas celdas lee la vía lenta) | sí (otra curita puede bajarla a 1) |
| b | REFERENCIA POR HERMANA | `par_herm ← True` para la próxima vida (usa el patrón de una hermana como referencia declarada) | sí |
| c | VORAZ | `voraz ← 1.0` (el emisor anota TODO lo que descubre, ERR-51 de bloque 4b) | sí |
| d | NADA | no toca nada. Curita por defecto y única del control `alma_ninguna` | — |

### Nivel 6 (planificación: mapa y dos metas) — instrumento del mapa/rodeo (`nivel6_mapa`, `nivel6_rodeo`)
| id | nombre | qué toca | reversible |
|---|---|---|---|
| a | AMPLIAR RETINA | `r_vis ← r_vis+1` (perilla ya usada, tope 5) | sí |
| b | ALARGAR MEMORIA DE COMIDA | `memoria_rechazo ← memoria_rechazo+10` | sí |
| c | NADA | — | — |

### Nivel 7 (composición de ≥ 3 órganos) — instrumento `mundo_temporal_k*.py`
| id | nombre | qué toca | reversible |
|---|---|---|---|
| a | SUBIR k | `k_max ← k_max+1` (perilla del mundo temporal, hasta el tope ya medido 3) | sí |
| b | BAJAR DISTRACTORES | `n_distractores ← max(n_distractores-1, 0)` | sí |
| c | NADA | — | — |

### Nivel 8 (aprendizaje abierto: desaprende + sorpresa acelera) — combina `organismo_familias`/`v15f` (desaprender)
con el predictor de `nivel9_allostasis` (sorpresa)
| id | nombre | qué toca | reversible |
|---|---|---|---|
| a | MEMORIA DE PARES | `memoria_pares ← True` (tabla v15f que ya separa variantes 7–7.5/8) | sí |
| b | SORPRESA EN LA BOCA | `k_sorp ← 0.5` (perilla ya existente de `organismo_vivo_h1`/allostasis; bloque 6 la puso en la tasa `eta`, REFUTADA — aquí se prueba en la boca, no en `eta`, siguiendo C-P1 del día 7) | sí |
| c | NADA | — | — |

### Nivel 10 y 11 — **sin menú**: no hay instrumento que declare esas perillas todavía (§0). El alma no puede
curar una perilla que no existe; proponerla sería "cambio de código", prohibido por la cláusula del menú
cerrado. Este preregistro los deja **fuera de alcance de ejecución** y dentro de alcance de **predicción**
(§4): dónde se espera que la escalera se atasque y por qué.

## 4. Predicción numérica, por brazo, ANTES de correr

Tres brazos por nivel disponible (5–9): **alma razonada** (yo, leyendo `alma_pregunta_<n>.json` y escribiendo
`alma_respuesta_<n>.json` con motivo), **alma aleatoria** (elige uniforme entre las entradas del menú de ese
nivel, sin leer nada), **sin alma** (siempre "NADA"/f, control).

| nivel | con alma razonada | con alma aleatoria | sin alma |
|---|---|---|---|
| 5 | promueve en ≤ 10 vidas (letra ya pasada sin alma; la curita sólo debería acelerarla) | promueve en ≤ 20 vidas | promueve igual (la letra de bloque 5 YA pasa sin ninguna curita) — **control de que el menú no está inflando un nivel que ya estaba resuelto** |
| 6 | promueve en ≤ 15 vidas | promueve en ≤ 25 vidas | promueve igual (letra ya replicada sin alma) |
| 7 | promueve (k=3) en ≤ 15 vidas | ≤ 30 vidas | promueve igual (ya medido 20/20 por k sin alma) |
| 8 | **primera vez que "desaprende ≥ 6/8" y "sorpresa acelera" se miden juntos**: predicción abierta, criterio de refutación = si conjunta cae por debajo de cualquiera de los dos por separado, el problema es la combinación, no cada mecanismo | igual que razonada menos frecuente | ninguno de los dos pasa el sub-criterio de sorpresa (ya refutado solo) |
| **9** | **promueve (R₀ ≥ 0.90) en ≤ 40 muertes, SI Y SÓLO SI condicionar la curita al historial del linaje aporta algo que fijar la herencia para todo el run (H-1) no tenía** — predicción cauta porque H-1 ya refutó las cuatro herencias fijas | **no promueve en 100 muertes** (elige entre las mismas seis curitas que H-1 ya barrió una por una sin éxito; al azar no hay condicionamiento al historial, que es la única palanca nueva) | **nunca promueve** (es literalmente repetir H-1: `hereda` fijo en 'nada', ya medido 0.148/0.140) |

**Predicción de dónde se atasca cada brazo, y por qué (compromiso central del encargo):**
- **Sin alma:** los cuatro brazos con instrumento (5, 6, 7 corren y promueven porque su letra YA está pasada sin
  ninguna curita; 8 se atasca en la mitad "sorpresa acelera" porque bloque 6 ya la refutó sola; **9 se atasca y
  no sale nunca**, repitiendo H-1 exactamente.
- **Alma aleatoria:** 5–7 promueven, más lento que la razonada, por las mismas razones que sin alma (ya estaban
  resueltos) más ruido. 8 se atasca igual que sin alma la mitad de las veces. **9 se atasca**: elegir al azar
  entre seis curitas ya individualmente refutadas no genera la condicional-al-historial que podría salvarlo.
- **Alma razonada:** 5–7 iguales o algo más rápidos que al azar (el techo ya estaba puesto por la letra, no por
  el alma). 8 es la primera medida real de la combinación. **9 es la apuesta**: si razona ("el linaje lleva 3
  muertes seguidas sin nacimiento → conectar al nodo Y subir la dote a la vez, no una sola cosa fija todo el
  run") puede cruzar 0.90; si no, **10 y 11 quedan fuera de alcance por dos razones independientes: el
  instrumento no existe (§0) Y el nivel 9, que los precede, no se sostiene (H-1 + esta réplica)**.

## 5. Qué refuta

- Si el alma **aleatoria** promueve el nivel 9 igual que la razonada (dentro de ±1 muerte del umbral, regla 12
  de `EQUIPO.md`), **las curitas no aportan razonamiento: era el nodo/la reencarnación, no el motivo** — se
  registra como hallazgo, no se declara alma "inteligente".
- Si **nadie** promueve el nivel 9 en 100 muertes con ninguno de los tres brazos, el cuello es **el mundo H-1**
  (ERR-62 confirmado con una búsqueda mucho más rica), y la escalera espera a que un cuerpo aprenda en una
  vida (nivel 8) antes de que la reproducción tenga algo que transmitir — la lectura que ya adelantó el cierre
  de H-1.
- Si el nivel 8 conjunto pasa pero cualquiera de sus dos mitades por separado seguiría fallando fuera del
  conjunto (falso positivo de interacción), se declara con la salvedad y una réplica antes de subir a 9.

## 6. Controles y medidas

**Controles por nivel (5–9):** alma razonada, alma aleatoria (misma semilla de rng que la razonada +1, para
que la única diferencia sea el criterio de elección), alma ninguna (curita "NADA"/"f" siempre — repite el
comportamiento sin alma del instrumento, es el mismo control que ya usa `MENU_curitas.md`).

**Medidas, iguales en los cinco niveles:**
- vida por cuerpo (pasos hasta esa muerte/fin de vida)
- R₀ del linaje (nivel 9: el que ya define `organismo_vivo_h1`/H-1; niveles 5–8: proxy = tasa de la letra de
  ese nivel por vida, ya que no hay linaje)
- nivel alcanzado (5, 6, 7, 8, 9 — o "no promovió")
- número de muertes/vidas hasta promover, o hasta agotar el presupuesto (100 para 9, 30 para 5–8)

## 7. Cláusula del buscador (idéntica a la de `MENU_curitas.md`, extendida a toda la escalera)

Lo que el alma encuentre en cualquier nivel **no es un resultado**: es una hipótesis — "la secuencia de curitas
X sube el nivel N". Cuenta sólo si se reproduce **sin alma**, perillas fijas desde el paso 0, preregistro nuevo,
semillas nuevas, y con `Pool` a cargo del coordinador (regla 3 de `EQUIPO.md`: este documento y su runner corren
en **un proceso**, nunca `multiprocessing.Pool`).

## 8. Humo (obligatorio antes de cualquier serie)

**1 semilla (seed=1), nivel 5, 10 muertes/vidas, alma razonada = el diseñador de este documento**, leyendo
`alma_pregunta_1.json` … `alma_pregunta_10.json` y escribiendo `alma_respuesta_1.json` … con el `id` elegido del
menú del nivel 5 (§3) y un motivo de una línea. Un proceso, `T` reducido para que el humo corra en minutos.
Salida: `experimentos/nivel13_alma/humo_eras_nivel5_YYYYMMDD.json` + la tabla de la §9 pegada aquí después de
correrlo.

---

## 9. Tabla del humo (corrida real, 18 sep 2026, 20:20–20:22)

`corre_eras.py --nivel 5 --alma razonada --vidas 10 --seed 1 --forzar_n_vidas --timeout 300`, un proceso,
`sha16` de `corre_eras.py` en el momento de correr: `7623721fbb06c11b`. `--forzar_n_vidas` se usó para poder
mostrar las 10 vidas completas del humo (sin él, el criterio de humo del §8 corta apenas 3 vidas seguidas con
`com=1`, que ya ocurrió en la vida 3 — ver §10). Yo fui el alma: leí cada `alma_pregunta_<n>.json` y escribí
`alma_respuesta_<n>.json` con un motivo de una línea, dentro del menú cerrado del nivel 5 (§3).

| vida | seed | com (letra CANAL, proxy) | racha | curita elegida | motivo |
|---|---|---|---|---|---|
| 1 | 1001 | 1 | 1 | d NADA | letra ya resuelta sin alma; no tocar antes de ver si se sostiene |
| 2 | 1002 | 1 | 2 | d NADA | estable, seguir sin tocar |
| 3 | 1003 | 1 | 3 | a SUBIR GANADORAS | perturbación controlada de robustez, no por necesidad |
| 4 | 1004 | 1 | 4 | d NADA | `k_ganadoras=2` no rompió nada; volver a NADA |
| 5 | 1005 | 1 | 5 | c VORAZ | segunda perturbación controlada, cubrir el menú |
| 6 | 1006 | 1 | 6 | b REFERENCIA POR HERMANA | `voraz=1.0` tampoco rompió nada; tercera perturbación |
| 7 | 1007 | 1 | 7 | d NADA | las tres perturbaciones (a, c, b) no rompieron `com=1`; cerrar en NADA |
| 8 | 1008 | 1 | 8 | d NADA | — |
| 9 | 1009 | 1 | 9 | d NADA | — |
| 10 | 1010 | 1 | 10 | d NADA | racha 10/10, cierre del humo |

`knobs` acumulados al final: `k_ganadoras=2, par_herm=('A','C'), voraz=1.0` — las tres perturbaciones quedaron
activas y `com=1` se sostuvo en las 10/10 vidas, con y sin cada una.

## 10. Tres líneas honestas

1. **El nivel 5 no midió nada nuevo hoy**: `com=1` en 10/10 vidas desde la vida 1, con el menú de curitas
   completo probado y sin romper nada — confirma lo que el registro ya sabía (bloques 4b/5 REPLICADOS) y no
   añade evidencia de que el alma "ayude": aquí no había nada que curar. El criterio de humo (§8, racha ≥ 3)
   se cumplió en la vida 3, dos vidas antes de que yo empezara a perturbar; usé `--forzar_n_vidas` para poder
   mostrar las 10 vidas y ejercitar las cuatro entradas del menú, no porque el nivel lo necesitara.
2. **El instrumento de nivel 9 (`organismo_vivo_h1.py`) no corrió hoy**: el humo obligatorio (§8) era del nivel
   5 por diseño (el más barato y ya resuelto, para probar el CABLEADO del bucle alma, no el organismo difícil);
   el runner de nivel 9 (`corre_nivel9`) está escrito y usa el menú heredado de `MENU_curitas.md`, pero **no se
   ejecutó** en esta entrega — es la corrida que de verdad puede contradecir ERR-62, y no se improvisa sin el
   presupuesto de tiempo y sin que el bucle base del otro creador (nodo central, curita (b)) exista de verdad;
   mi `corre_nivel9` hoy no puede aplicar la curita (b) (SUBIR EL MIEDO) porque necesita el nodo, que todavía
   no es un módulo importable — se registra como limitación, no se simula un nodo falso para no ensuciar la
   medida.
3. **Los niveles 10 y 11 no tienen instrumento, y eso es un hallazgo, no un vacío de este documento**: nadie en
   el proyecto ha construido un organismo que junte canal (nivel 5) con herencia por muerte (nivel 9) en el
   mismo cuerpo, y ninguna perilla existente permite que un cuerpo invente un token que el mundo no le dio
   (nivel 11). El menú cerrado del alma (regla del proyecto: nunca cambios de código) hace explícito que **el
   alma no puede subir la escalera más allá de donde hay perillas** — subir de 9 a 10 exige primero que un
   creador construya el instrumento, no otra curita.

---

## Anexo — hashes y nota de cierre

- `corre_eras.py`: `7623721fbb06c11b` (sha256 corto, corrida del humo §9).
- `PREREGISTRO_eras.md` (este archivo): `e4b74584968ebae5`.

**Nota añadida al cerrar el humo (18 sep 2026, ~20:25):** mientras corría este documento, el bloque ALMA base
del otro creador apareció en la misma carpeta (`organismo_alma.py`, `corre_alma.py`, `alma_aleatoria.py`,
`alma_ninguna.py`, `PREREGISTRO_alma.md`). Su interfaz real es `alma_io/alma_pregunta_<sem>_<n>.json` /
`alma_io/alma_respuesta_<sem>_<n>.json` (subcarpeta `alma_io/`, nombre con la semilla) — **no**
`alma_pregunta_<n>.json` en la carpeta de trabajo, como decía literalmente el encargo y como asumió el fallback
de `corre_eras.py` (documentado arriba como tal). Además `organismo_alma.py` es su propio organismo (con el
menú de `MENU_curitas.md` cableado dentro), no una librería genérica importable por nivel (`escribe_pregunta`/
`lee_respuesta`) — el intento de `_intenta_importar_base_alma()` en `corre_eras.py` no lo encontrará con los
nombres que prueba hoy. **No se editó nada de esos archivos.** Para el nivel 9, lo correcto de aquí en adelante
es NO reimplementar un bucle propio (como hace hoy `corre_nivel9`, con la limitación ya declarada en §10.2) sino
**correr directamente `corre_alma.py`** del otro creador (que ya implementa exactamente el menú de
`MENU_curitas.md` sobre `organismo_alma.py`) para el nivel 9, y reservar `corre_eras.py` para orquestar la
escalera completa llamándolo como subproceso o import una vez que su interfaz se confirme estable. Se deja
escrito como el siguiente paso, no se ejecuta hoy: cambiar la integración después de ver el código ajeno sin
antes preregistrar el cambio sería recalibrar (regla 3 de `CLAUDE.md`).
