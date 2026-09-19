# MENÚ CERRADO DE CURITAS — nivel 13, BLOQUE ALMA (escrito ANTES de correr nada, 18 sep 2026)

MISIÓN: llegar a la AGI por este camino — un organismo mínimo con reglas locales que aprende, sobrevive, se
comunica y se reproduce; con evidencia preregistrada. Hoy: un "alma" externa que parcha al cuerpo cada vez que
muere, sin confundir el buscador con el resultado.

Este archivo fija **el espacio de acción del alma**. El alma (un agente Haiku, o el diseñador jugando de alma en
el humo, o un control automático) elige **exactamente UNA** entrada por muerte. Cualquier respuesta fuera de este
menú es un error del instrumento y aborta la corrida (`raise SystemExit`). El menú NO se amplía después de ver
datos: ampliarlo es un ERR numerado + semillas nuevas (regla 4 y 11 de `registro/EQUIPO.md`).

## Las seis entradas

| id | nombre | qué toca exactamente | reversible |
|---|---|---|---|
| **a** | CONECTAR AL NODO | pone `conectado = True` para **todos los cuerpos siguientes**: al nacer leen el nodo central como exposiciones SIN consecuencia | no (una vez conectado, el linaje queda conectado) |
| **b** | SUBIR EL MIEDO | escribe en el nodo `miedo_n = 5` copias del mensaje `(patrón del estímulo que precedió a la muerte, R = −3.0, necesidad activa en esa mordida)` | no (el nodo no se borra) |
| **c** | DOTE MAYOR | `dote ← min(dote + 0.1, rep_umbral − 0.05)` (perilla del mundo: lo que el padre paga al hijo) | sí (otra curita puede no volver a subirla; no hay curita que la baje) |
| **d** | BAJAR EL UMBRAL | `rep_umbral ← max(rep_umbral − 0.1, dote + 0.05)` (perilla del mundo: qué tan saciado hay que estar para abrir ventana de reproducción) | sí (no hay curita que lo suba) |
| **e** | HEREDAR VALORES | `hereda ← 'M1'` para todos los partos siguientes (el hijo recibe el VECTOR `Wps/Wns` del padre; es el brazo M1 de H-1) | no |
| **f** | NADA | no toca nada. Es la curita por defecto y la única del control `alma_ninguna` | — |

## Invariantes que el instrumento impone (no son decisiones del alma)

- `0 < dote < rep_umbral` en todo momento (guardia de H-1: pagar la dote no puede matar al padre). Las curitas (c)
  y (d) están **acotadas** por los `min`/`max` de la tabla, así que no pueden violarla.
- El nodo se **llena siempre** (mientras `nodo = 1`) con las últimas `nodo_k = 20` mordidas con consecuencia del
  cuerpo que acaba de morir, **elija lo que elija el alma**. Lo que la curita (a) cambia es **quién lo lee**.
  ("las células que quieren vivir se conectan y reciben los datos, las que no, que se mueran solas" — el director.)
- La curita (b) es la única que **escribe** en el nodo algo que no salió de una mordida real: es un mensaje
  fabricado por el alma. Por eso lleva su propio contador y se reporta aparte (`curitas`).
- Si el cuerpo que murió no mordió **nada** en toda su vida, (b) cae sobre su última **exposición**; si tampoco
  hubo exposición, (b) es inerte y se registra como tal.
- Ninguna curita toca pesos del organismo directamente (ERR-44: conducta, no pesos). (a) y (b) actúan por el
  **canal** (exposición sin consecuencia); (c), (d) son perillas **declaradas del mundo**; (e) es una perilla de
  herencia que H-1 ya midió.

## Qué NO está en el menú (y por qué)

- Cambiar `eta`, `eta_s`, `puerta`, `alpha`, `aversion` o cualquier constante del organismo: sería el alma
  buscando hiperparámetros, no parchando al cuerpo — y el resultado no sería transferible a un mundo sin alma.
- Cambiar el mundo (`nobj`, `costo`, `tipos`): H-1 ya barrió esa rampa y la declaró búsqueda, no evidencia
  (ERR-62). Si el alma pudiera abaratar el mundo, "sobrevive más" sería trivial.
- Escribir directamente en `Wp/Wn/Wps/Wns` del hijo: eso es copiar pesos, no comunicar (ERR-44).

## Cláusula del buscador (regla que manda sobre el resultado)

Lo que el alma encuentre **NO es un resultado**. Es una **hipótesis**: "la secuencia de curitas X sostiene el
linaje". Para que cuente hay que volver a correr ese punto **sin alma**, con las perillas fijas desde el paso 0,
con preregistro nuevo y semillas nuevas. El alma es el buscador (como JUACO-EVO fue el buscador de la división
por conflicto de signo); el resultado es lo que sobrevive sin él.
