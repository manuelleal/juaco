---
name: juaco-bloque
description: Corre un bloque preregistrado de JUACO de principio a fin con el protocolo completo (preregistro commiteado, Pool libre, humo, serie, registro, commit, push). Úsala con /juaco-bloque <ruta del PREREGISTRO o del corre_*.py> o cuando Christiam diga "corre el bloque", "lanza la serie", "dale parejo con X".
---

Bloque: $ARGUMENTS

Repo: la raíz de este repositorio (en el PC del director: `C:\Users\User\Documents\PROYECTOS\JUACO\bundle`; en la nube: el directorio de trabajo). Protocolo (reglas 3, 4, 11, 12 y 14 de `registro/EQUIPO.md`); no saltar pasos, cada uno deja rastro en el log:

1. **Problema antes de actuar.** Escribe en dos líneas qué problema resuelve el bloque y qué podría fallar (instrumento, criterio, comparador). Si el preregistro no tiene predicción numérica, control que pueda fallar y semillas NUEVAS, no se corre: se devuelve al agente `juaco-creador`.
2. **Preregistro commiteado ANTES de correr.** `git log -1 -- <preregistro>`; si no está, `git add` + `git commit` sólo del preregistro y del instrumento.
3. **Identidad.** Salida del arnés pegada en el preregistro o corrida ahora en un proceso (el agente `probador-haiku` puede hacerlo). Perillas apagadas = tronco bit a bit; los controles que deben fallar, fallan.
4. **Entrada campo a campo** de cualquier batería copiada contra la del tronco (ERR-38, ERR-41).
5. **Pool libre.** Procesos python vivos con cmdline (ver skill `juaco-estado`, paso 3). Si hay otro Pool, esperar; nunca matar procesos (ERR-85). Fijar `JUACO_POOL` o `--pool` según la CPU libre (ERR-86: Pool(14) con otras corridas da BrokenPipe).
6. **Humo** que ESCRIBA su JSON (`--humo`, semilla fuera de la serie). Si no escribe JSON, no hay serie (ERR-42).
7. **Serie** con las semillas del preregistro, en segundo plano, con log. Mientras corre, no lanzar otro Pool.
8. **Lectura.** Veredicto por la letra del preregistro desde el JSON de precisión completa (no del log). Si un veredicto depende de UNA semilla en el umbral, réplica automática en rango nuevo (regla 12). Subconjuntos sólo con enmienda previa (regla 10).
9. **Registro.** Encargar al agente `juaco-cronista` la entrada del registro con log + JSON; revisar sus números contra el JSON antes de pegar.
10. **Commit + push** con crudos, log, JSON, preregistro y registro. Mensaje en el estilo del repo.
11. **Reporte al director** con el formato de la skill `veredicto`.

Si algo cae por el instrumento y no por el organismo, se numera ERR (skill `juaco-err`) y el reintento va preregistrado en la misma sesión.
