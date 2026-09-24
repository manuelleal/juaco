EXPLORATORIO — no es dato

# Prototipos exploratorios de la nube — noche del 23→24-sep-2026

> Libertad para experimentar dada por el director para esta noche (`NUBE.md` §2b, punto 3). **Nada de aquí es dato ni sube un
> nivel**: sirve para decidir qué se preregistra. Cada número lleva su comando y su semilla.
>
> **Reglas de esta carpeta:**
> - Semillas exploratorias **24001–24099** (grep del 24-sep: ningún paquete las usa). No deben reutilizarse en series confirmatorias.
> - Un proceso a la vez, en el núcleo que dejan libre las series (Pool 3).
> - No se toca ningún archivo de la carrera ni del tronco: todo son subclases o copias, construidas aquí.

## Instrumento
- **Pista:** la de la carrera del 22-sep sin tocar (`carrera_escuderias/pista.py` 9f47c65e438e0ff4). Monocultivo de 9 carros,
  escala 1 (L 360, 36 objetos), pizarra 1, `fundador_limpio=1`. Es la misma entrada que `juez.tarea` y `corre_v143.tarea`.
- **Juez:** `juez.resumen_linaje` (6a68f640a7832f12). Las medidas salen sólo de la física (ERR-96).
- **Corredor:** `corre_explora.py`.
- **Identidad:** `corre_explora.py --identidad` comprueba que la subclase sin reglas (W0) es FABRICA bit a bit, en toda la física de
  los 9 linajes y la pista (semillas 24098 y 24099, T 3000). Resultado: **OK** (01:50 UTC).

## (i) Arriesgar según la reserva
Carros en `carros_reserva.py` (NEO, LIM) y `carros_extra.py` (NEO, MAL, LIM con la función `aplica`, también sobre APR en
`carros_apr_reserva.py`). Todos son subclases: dejan correr la boca del carro base (mismo consumo del rng) y sólo corrigen la
decisión final. La reserva es r = min(E, Ag).

**Tanda i1** (01:50–02:04 UTC):
`python experimentos/exploratorio_nube_20260924/corre_explora.py --brazos FAB,NEO5,LIM,NEO5_LIM,O1 --desde 24001 --n 6 --T 30000 --tag i1`
Semillas 24001–24006, T 30 000. JSON: `datos/explora_i1_FAB-NEO5-LIM-NEO5_LIM-O1_s24001-24006_T30000_20260924_015047.json`.

| brazo | R0 real (mediana) | persisten | vida | muere sin parir | gana a FAB (pareado) |
|---|---|---|---|---|---|
| FAB | 0.149 | 1/54 | 66 | 0.89 | — |
| NEO5 (no prueba lo desconocido si r < 0.5) | 0.133 | 1/54 | 66 | 0.90 | 1/6 |
| LIM (limpia lo malo si r ≥ 1.4) | 0.033 | 0/54 | 70 | 0.97 | 0/6 |
| NEO5_LIM | 0.033 | 0/54 | 70 | 0.97 | 0/6 |
| O1 | 0.775 | 20/54 | 3454 | 0.25 | 6/6 |

Lectura:
- **La neofobia sola no ayuda.** Lo desconocido es poco: el 12 % de los encuentros en la semilla 24001.
- **Limpiar desde 1.4 hunde el R0.** El golpe deja el nivel en 1.0, y al paso siguiente el costo lo baja de la ventana de parto
  (hacen falta E y Ag ≥ 1.0 durante 500 pasos seguidos). El que limpia pierde su parto.
- **El 72 % de los encuentros de FABRICA son con objetos que su valor ya marca como malos.** Semilla 24001: 17 706 de 24 682.
  De ahí salen las variantes MAL (no morder lo malo conocido con reserva baja) y VER (tema iii).

**Tanda i2** (02:06–02:32 UTC, nice 19):
`python experimentos/exploratorio_nube_20260924/corre_explora.py --brazos FAB,MAL14,MALINF,RES,VER,VER_MAL,VER_RES,APR,APR_RES --desde 24001 --n 6 --T 30000 --tag i2`
Identidad previa: 12/12 OK (W0, W2, WP, WV == FAB; WA == APR; RESP == RES; semillas 24098–24099).

| brazo | R0 real | persisten | vida | muertes | mord. B+D | pasos sin nada bueno | gana a FAB |
|---|---|---|---|---|---|---|---|
| FAB | 0.149 | 1/54 | 66 | 116 | 465 | 0.000 | — |
| MAL14 (no muerde lo malo si r < 1.4) | 0.097 | 2/54 | 200 | 42 | 45 | 0.127 | 0/6 |
| MALINF (nunca muerde lo malo) | 0.133 | 2/54 | 200 | 44 | 41 | 0.126 | 2/6 |
| RES (neo 0.5, mal 1.45, limpia ≥ 1.45) | 0.116 | 7/54 | 200 | 47 | 52 | 0.082 | 0/6 |
| VER (objetivo por valor) | 0.136 | 2/54 | 77 | 114 | 468 | 0.001 | 2/6 |
| VER_MAL | 0.110 | 2/54 | 200 | 44 | 43 | 0.178 | 1/6 |
| VER_RES | 0.089 | 8/54 | 200 | 49 | 52 | 0.109 | 1/6 |
| APR | 0.118 | 6/54 | 66 | 110 | 453 | 0.001 | 1/6 |
| APR_RES | 0.116 | 7/54 | 200 | 48 | 52 | 0.082 | 0/6 |

Lectura:
- **Ninguna variante le gana a FABRICA en R0 real.**
- **Las reglas que vetan lo malo sí cumplen lo que prometen, pero el mundo se tapa.** Bajan las mordidas malas a la décima parte y
  las muertes a menos de la mitad. Sin mordidas de lo malo, nada lo quita del mundo (sólo el olvido): hasta el 18 % de los pasos no
  hay nada bueno en ninguna parte. El cuerpo muere de hambre a los 200 pasos exactos: una mordida mala al nacer lo deja en 0.2, y
  0.2 / 0.001 = 200.
- **VER no reduce las mordidas malas.** En un anillo, el camino hacia lo bueno pasa por encima de lo malo, y la boca con hambre lo
  muerde igual.
- **La limpieza es un bien público.** FABRICA muerde todo: mantiene el mundo limpio y muere joven. Si veta lo malo, se muere de hambre.
  O1 lo resuelve limpiando sólo cuando no queda nada útil y el golpe es costeable. Eso se prueba en i3 con el valor aprendido del
  bicho (`carros_limpia.py`).

## (ii) Aprender prediciendo
_(pendiente)_

## (iii) Propio
_(pendiente)_
