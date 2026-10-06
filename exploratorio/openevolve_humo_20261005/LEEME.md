# Humo de OpenEvolve contra la pista y el juez de JUACO (5-oct-2026) — EXPLORATORIO, nada se declara

Qué es: evolución de PROGRAMAS guiada por un modelo de lenguaje (OpenEvolve, proveedor claude_code), con la pista y el juez de JUACO como evaluador, sin tocarlos. No es selección natural del organismo. Un solo humo de 30 rondas; sin réplica; sin los controles que exigiría una serie (búsqueda al azar con el mismo presupuesto, modelo más débil, varias corridas independientes).

Punto de partida (`raiz/programa_inicial.py`): O1 con la limpieza quitada y sin comentarios que la delaten; colapsa. Fundador NO limpio (ERR-191). Preregistro del humo: `PREREGISTRO_humo.md` (escrito antes de correr).

Búsqueda (semillas de búsqueda; `humo/consola_err.txt`, `humo/evaluaciones.jsonl`): rondas 1–11, ningún programa cruza; ronda 12, 3/9; ronda 13, 6/9; ronda 28, 8/9; ronda 30, 9/9. 14 de 30 programas cruzan 6/9 o más.

Examen en semillas selladas (T 100 000, fundador no limpio; `examen/examen.log`), dos semillas completas al cerrar:

| programa | semilla 272001 | semilla 272002 |
|---|---|---|
| MEJOR (criado por la herramienta) | persisten 9/9, cruzan 9/9, R0 0.963 | persisten 9/9, cruzan 7/9, R0 0.963 |
| O1 (escrito a mano) | persisten 9/9, cruzan 7/9, R0 0.933 | persisten 6/9, cruzan 5/9, R0 0.950 |
| RAIZ (punto de partida) | 0/9, 0/9, R0 0.157 | 0/9, 0/9, R0 0.250 |

El mejor programa pasa el filtro estático de reglas. Lo que escribió (leído por el coordinador en el punto de control 25): una regla para morder letras malas conocidas cuando hacerlo deja la reserva por encima de un piso de seguridad y no está en zona de reproducción ("reciclar renueva el stock del mundo"), es decir, la limpieza de O1 redescubierta con su piso; además llena la reserva hasta el tope real y no persigue comida lejana cuando ya está bien.

Reservas obligatorias:
- Dos semillas de examen: orienta, no declara. Mayoría (≥ 5/9) en 2 de 2 para MEJOR y para O1.
- Otro régimen que O1: muerde lo malo 2.7 veces más (9 031 y 9 091 contra 3 349 y 3 423), vive menos (vida mediana 2 405 contra 4 039) y deja el mundo "sin nada bueno" el 24 % del tiempo contra el 4 %. No se sabe si eso es mejor o sólo distinto.
- El que propone es un modelo de lenguaje con conocimiento general: "limpiar lo que estorba" puede venir de ahí y no de la búsqueda. Lo decide el control con búsqueda al azar y con un modelo más débil, no corridos.
- Sin informe del agente al cerrar (apagado del PC); este LEEME lo escribió el coordinador desde los registros.
