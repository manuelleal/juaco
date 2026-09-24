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
_(en curso)_

## (ii) Aprender prediciendo
_(pendiente)_

## (iii) Propio
_(pendiente)_
