---
name: juaco-err
description: Registra un ERR nuevo en JUACO (error de instrumento, criterio, lectura o procedimiento) con el siguiente número libre, en el formato del repo. Úsala cuando se detecte un fallo del instrumento, se cambie un umbral o criterio, o Christiam diga "eso es un ERR", "numera eso", /juaco-err <descripción>.
---

Qué pasó: $ARGUMENTS

Repo: la raíz de este repositorio (en el PC del director: `C:\Users\User\Documents\PROYECTOS\JUACO\bundle`; en la nube: el directorio de trabajo).

1. Siguiente número libre:

       grep -oh "ERR-[0-9]*" registro/*.md registro/investigacion/*.md experimentos/*/*.md | sort -t- -k2 -n | tail -1

2. Formato de la entrada (copiar el de la última ERR del registro): **ERR-NN (fecha hora):** qué se observó · causa (instrumento / criterio / lectura / procedimiento) · qué veredictos ya registrados toca (verificado contra los JSON, no asumido; "ninguno" si es así) · corrección · regla nueva si la hay (numerarla en `registro/EQUIPO.md`).
3. Reglas fijas: toda enmienda que cambie un umbral o la forma de un criterio lleva ERR al escribirla (regla 11); nunca se recalibra sobre los datos ya vistos: criterio nuevo + semillas nuevas.
4. Dónde va: entrada en `registro/REGISTRO_etapas_1_2.md`, línea en la sección vigente de `registro/HANDOFF.md`, y si nace una regla, `registro/EQUIPO.md`. Si el ERR afecta a un instrumento, comentario en el código con el número.
5. Si un veredicto registrado cambia, se dice explícitamente en el registro y en el commit; si no cambia, también ("el veredicto no cambia, verificado contra X").
6. Commit sólo del ERR y su corrección, con mensaje que empiece por "ERR-NN:".
