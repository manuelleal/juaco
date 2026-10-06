# PROPUESTA (no preregistrada) — de PRENDER órganos a CREARLOS. Para trabajarla en local con Claude Code (nube, 24-sep-2026)

Misión: llegar a la AGI por este camino. Esto NO es un preregistro: es el diseño para que el director lo construya en su PC.
El resumen está también en `registro/NUBE_BITACORA_20260924.md` §4.

## Dónde estamos
- **ECO v2.1 FUNCIONA ×2** (`PREREGISTRO_eco_v21.md`, datos `datos/eco_v21_*`): un órgano que nace APAGADO en todos los cuerpos
  (`ensena`: el padre pasa su tabla al hijo al nacer) lo prende sola la selección en los tres mundos (97–99 % del banco de VIDA contra
  12–47 % de AZAR; ~100 % de los vivos al final).
- Pero el órgano lo diseñamos nosotros: el gen es un interruptor con umbral (≥ 1.0 se expresa). **La selección elige; no inventa.**
- Para que invente, el genoma tiene que describir **cómo se construye** el órgano, no sólo si está prendido.

## Criterio de "creó un órgano" (escribirlo ANTES de correr)
El órgano que gana (el que expresa el banco de VIDA en el corte) **no está en la lista de los diseñados** y **les gana a todos** en un
juez de colonias con placebo (como el de ECO v1.1). Si la selección sólo reencuentra un punto que escribimos, no creó nada.

## Palanca 1 (la recomendada): órganos de transmisión armados con piezas
El canal ya existe y no hay que tocar el motor: el padre arma un mensaje en `al_parir` y el hijo lo recibe en `nace`.
- `carros/FAMB_ORG_ECO.py` ~257 `al_parir`: arma la TABLA (por patrón y necesidad, la R más reciente vivida; si no la vivió, la heredada)
  y la devuelve. `ENSENA` apagado → `None` (el hijo no recibe nada).
- `carros/FAMB_ORG_ECO.py` ~283 `nace`: `FILTRA0` del hijo quita las entradas con R = 0; luego el nodo del hijo = la tabla × `NODO_LEE`.
- Los genes vienen del genoma de cada cuerpo (`kw`, línea ~72). Los órganos nuevos se añaden como en `construye_eco_org.py` (por anclas,
  con arnés que compruebe que con los valores de fábrica todo es bit a bit igual a `FAMB_ORG_ECO`).

Piezas propuestas (cada una un gen; las de umbral se expresan si ≥ 1.0, todas nacen en el valor que reproduce a `ensena`):
| lado | pieza | qué hace | punto diseñado |
|---|---|---|---|
| padre | `pasa_malas`, `pasa_buenas`, `pasa_neutras` | incluye en el mensaje las entradas con R < 0, R > 0, R = 0 | las tres prendidas (= `ensena`) |
| padre | `mag_min` (continuo) | sólo pasa entradas con \|R\| ≥ mag_min | 0 |
| padre | `solo_vivido` | sólo lo que el padre vivió, no lo que heredó (el código ya tiene el modo `res1`) | apagado |
| hijo | `dosis` (continuo → entero 1..8) | cuántas copias de la tabla entran al nodo (hoy `NODO_LEE`) | el de fábrica |
| hijo | `filtra0` | ya existe | apagado |
| hijo | `invierte` | invierte el signo de lo recibido — **control de cordura: la selección debe tirarlo** | apagado |

Lista de puntos diseñados (la que el ganador NO debe estar): `ensena`; `ensena + filtra0`; `res1`. Todo lo demás cuenta como nuevo
(p. ej. "pasar sólo el veneno", "pasar sólo lo fuerte", "dosis alta de sólo lo malo").

Medidas: por pieza, O1\* (fracción que expresa en el real contra la media de sus 8 sombras, del checkpoint del corte) y O2 (VIDA contra
AZAR), como en v2.1; la combinación modal del banco de VIDA en el corte; y el juez de colonias: la combinación ganadora contra cada punto
diseñado, con placebo (otra muestra del mismo banco) válido en [5, 15].

Costo estimado: Python, w30, T 120 000: ~3 min por corrida → 40 corridas (20 semillas × VIDA/AZAR) ≈ 40 min con Pool 3; w90 con el
gemelo haría falta extenderlo (agente compilador).

## Palancas siguientes (en orden)
2. **Duplicar y divergir** (Ohno 1970): una mutación copia un "slot" de órgano; la copia deriva libre mientras el original mantiene la
   función; si la copia encuentra otra función, hay un órgano nuevo.
3. **Cablear órganos**: genes que conectan la salida de uno con la entrada de otro (que el interruptor decida cuándo se enseña; que la
   sorpresa decida qué se hereda).
4. **Que el lenguaje mismo crezca** (Avida, Tierra): evolución abierta. Lejos; no se promete.

## Trampas que ya costaron hoy (no repetirlas)
- **nube-8:** para un rasgo con umbral no sirve comparar la MEDIA del gen con sus sombras; hay que comparar la FRACCIÓN que lo expresa
  (del checkpoint del corte, con el banco de pares genoma–8 sombras). Ver `corre_eco_v21.py` `expresion_sombras`.
- **nube-9:** una guardia del motor (`SystemExit`, p. ej. ERR-60: más de 100 000 cuerpos en un linaje) dentro de un `Pool` mata al
  trabajador sin error visible y el `Pool` espera para siempre. Con familia, a T = 1e6 los linajes pasan ese límite (ECO v1.2 se colgó
  así). Atrapar `SystemExit` en el trabajo y devolverlo como fila con error; no pasar de T ~ 3e5 con familia sin cambiar las semillas.
- En AZAR el banco guarda el genoma NUEVO del hijo (`motor_eco3.py`:438 y 477; igual en motor_eco2): es deriva pura.
- Semillas nuevas con `grep` antes de fijarlas; el arnés en semillas de práctica, nunca en las de la serie ni en las del juez.
