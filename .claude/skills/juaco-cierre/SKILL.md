---
name: juaco-cierre
description: Cierre de jornada de JUACO. Deja todo registrado, commiteado, empujado y la memoria al día para que la siguiente sesión retome sin releer. Úsala cuando Christiam diga "cerremos", "cierre del día", "deja todo listo", "me voy", o invoque /juaco-cierre.
---

Notas del director para el cierre: $ARGUMENTS

Repo: la raíz de este repositorio (en el PC del director: `C:\Users\User\Documents\PROYECTOS\JUACO\bundle`; en la nube: el directorio de trabajo).

1. `git status --short`. Clasificar cada archivo: crudo/log/JSON de una corrida registrada (entra), instrumento verificado (entra), borrador sin identidad (entra marcado como borrador en el mensaje), basura (se lista, no se borra sin permiso).
2. Ningún Pool corriendo (procesos python con cmdline). Si hay uno, esperar a que termine o dejar dicho en el HANDOFF qué corre y desde cuándo.
3. Registro: toda corrida terminada hoy tiene su entrada en `registro/REGISTRO_etapas_1_2.md`. Las que falten: agente `juaco-cronista`.
4. `registro/HANDOFF.md`: nueva subsección "Cierre del <fecha>" con: corrido y registrado hoy · preparado y pendiente (con paquete verificado o no) · decisiones del director tomadas hoy (hora y palabras) · próximo candidato · ERR nuevos (rango) · quién retome lee X, Y, Z en ese orden.
5. `CLAUDE.md` bloque Estado: una línea nueva con el tronco vigente y el estado de fase.
6. Commit con mensaje en el estilo del repo + `git push`. Verificar `git status` limpio.
7. Memoria: crear `juaco-exo-estado-<fecha>.md` (o actualizar el vigente) y `juaco-proyecto.md` si cambió el tronco o el rumbo. Fechas absolutas. Actualizar el índice `MEMORY.md`.
8. Reporte final al director: tabla corta hecho / pendiente / decisión, y el comando exacto con el que arranca la siguiente sesión.
