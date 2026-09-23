---
name: juaco-estado
description: Estado actual de JUACO en una tabla corta (hecho / en curso / pendiente) con máximo dos decisiones para el director. Úsala al abrir sesión cuando Christiam diga "estamos en el proyecto juaco", "cómo vamos", "qué está pendiente", "revisa el estado", o invoque /juaco-estado.
---

Foco pedido: $ARGUMENTS (vacío = todo JUACO).

Repo: la raíz de este repositorio (en el PC del director: `C:\Users\User\Documents\PROYECTOS\JUACO\bundle`; en la nube: el directorio de trabajo). alefast (`PROYECTOS\JUACO-EXO`) es parte del proyecto pero tiene su propio repo: no se mezcla aquí; sólo se menciona si el director lo pide.

Pasos (todo con Bash, sin editar nada):
1. `git status --short` y `git log --oneline -8`.
2. Leer el bloque "Estado" más reciente de `CLAUDE.md`, la última sección de `registro/HANDOFF.md` (la 15.x más alta), el "ORDEN VIGENTE" más reciente de `registro/PLAN.md` y las últimas 40 líneas de `registro/REGISTRO_etapas_1_2.md`.
3. Procesos python vivos con cmdline (ningún bloque arranca si hay un Pool ajeno corriendo). Linux/nube: `ps -eo pid,args | grep [p]ython`. Windows (PowerShell):

       Get-CimInstance Win32_Process -Filter "name='python.exe'" | Select-Object ProcessId,CommandLine | Format-List

4. Contrastar con la memoria (`juaco-proyecto`, `juaco-exo-estado-*`) y anotar si la memoria está atrasada.

Salida, en este orden y en lenguaje llano:
1. Una línea de veredicto: VAMOS BIEN / VAMOS MAL / HAY ALGO MODESTO (ver skill `veredicto`).
2. Tabla: fila por frente, columnas Hecho · En curso · Pendiente · Bloqueo. Numerar con los niveles del brief y las fases del HANDOFF, nunca con fases inventadas.
3. Cambios sin commitear (lista de archivos y qué son).
4. Máximo DOS decisiones que le tocan al director, cada una con la opción recomendada primero.
5. Siguiente paso concreto con el comando exacto.

Si la memoria del proyecto quedó atrasada respecto al repo, actualízala al final (`juaco-proyecto.md` o un `juaco-exo-estado-<fecha>.md` nuevo) y dilo en una línea.
