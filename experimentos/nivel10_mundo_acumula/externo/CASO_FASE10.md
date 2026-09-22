# CASO DE ESTUDIO 2 — ¿Fable mejora con todos los poderes? (21-sep-2026)

Encargo del director: ver si Fable 5.1 razona mejor cuando tiene el exo (memoria compartida por consecuencia), un .md muy bueno y
aprendices Haiku; comparar también Haiku con esos poderes contra Fable; y al final entregar UN `.md` con la mejor solución al
encargo real de la fase 10 de JUACO (`ENCARGO_mundo_fase10_20260921.md`, copiado en esta carpeta).

## Brazos (misma especificación: el ENCARGO tal cual; misma copia de lectura del repo de JUACO)
| brazo | modelo | poderes | carpeta |
|---|---|---|---|
| F0 | Fable 5.1 | ninguno: el encargo y lectura del repo de JUACO | `equipos/fase10/F0_fable_solo/` |
| F+ | Fable 5.1 | `PODERES.md` + memoria del exo (`memoria_cli.py`, modo equipo) + aprendices Haiku (`aprendiz.py`) | `equipos/fase10/F1_fable_poderes/` |
| H+ | Haiku | los mismos poderes que F+ | `equipos/fase10/H1_haiku_poderes/` |

Ninguno escribe fuera de su carpeta; ninguno toca `PROYECTOS\JUACO\bundle` (sólo lectura); ninguno corre `Pool` ni series (sólo
humo de un proceso, ≤ 6 corridas, ≤ 200 000 pasos, como manda EQUIPO.md); ninguno lee `equipos/fase10/_evaluacion/`.

## Cómo se mide (escrito antes; 100 puntos)
| # | criterio | cómo se comprueba | puntos |
|---|---|---|---|
| 1 | **Aceptación del encargo (§5 del ENCARGO)** | arnés de identidad completo y pegado, con ≥ 7 controles que DEBEN diferir y difieren (8) · humo de un proceso que ESCRIBE su JSON en la carpeta del brazo (8) · cada puerta M10-1..M10-5 con nulo, margen y n declarados y el placebo entre los brazos (8) · predicciones con rango y probabilidad declarada, incluidas las que el autor cree que caerán (6) · nada del organismo modificado a mano para pasar una puerta (5) | 35 |
| 2 | **Requisitos del mundo (§2.1)** | los 6 requisitos con su número verificable escrito y, donde el humo lo permita, medido (recursos que se agotan; saber dónde vale tanto como saber qué; estímulos compuestos; cambios no avisados; varios cuerpos como opción; coste de vida con R₀ NADA 0.1–0.3 y RENACE 0.8–1.3). 3 puntos cada uno | 18 |
| 3 | **Método (§3)** | −3 por cada violación: recalibrar tras ver datos · criterio con umbral igual al nulo · batería copiada sin comparar campo a campo · semilla ya usada (grep) · vocabulario prohibido sin medida ("población", "cultura", "enseña", "entiende", "planifica") · tocar JUACO o `main` · correr `Pool`. Parte de 15 | 15 |
| 4 | **Las cuatro trampas (§2.4) y los fallos pasados (ERR-35..93)** | sección explícita que dice cómo el diseño evita cada trampa y qué ERR podría repetir; 1 punto por trampa cubierta, hasta 4 por ERR relevantes citados con su número | 8 |
| 5 | **Auditoría independiente** | `auditor-numeros` sobre el paquete: cada número del informe reproducible con un comando; 12 sin hallazgos graves, −4 por grave | 12 |
| 6 | **Uso de los poderes (sólo F+ y H+; F0 recibe la media de los otros dos)** | ¿la memoria del exo registró consecuencias y fue consultada antes de repetir algo? ¿los aprendices hicieron trabajo verificable y su salida se auditó antes de usarse? (registro `memoria_equipo.json` y `aprendices/*.md`) | 6 |
| 7 | **Coste** | tokens y tiempo se REPORTAN; el más barato con ≥ 60 puntos se lleva 6; el resto proporcional | 6 |

Umbral "paquete que el coordinador de JUACO aceptaría para gastar CPU": **≥ 70 con aceptación (criterio 1) ≥ 25/35**.

## Predicción del árbitro (antes)
F+ > F0 en criterios 3 y 4 (método y trampas: es lo que el .md aporta), igual o ligeramente mejor en 1 y 2, y más caro en tokens.
H+ queda por debajo de F0 en 1 y 2 (la construcción por anclas con identidad bit a bit es lo más duro) y por encima en 3 (más
disciplina). Refuta la tesis "los poderes mejoran a Fable": F+ ≤ F0 en total. Refuta "Haiku con poderes alcanza a Fable": H+ < 60.

## Entregable final para JUACO
`equipos/fase10/_evaluacion/PARA_JUACO_mundo_fase10.md`: la mejor solución, ensamblada por el árbitro con procedencia por sección
(qué brazo aportó qué), con los recortes de la auditoría, lista para que el director la lleve al repo de JUACO.

## Límites (antes)
- Una corrida por brazo, sin réplica. Los brazos F0 y F+ comparten modelo pero no contexto: F+ tiene más texto que leer (puede ayudar
  o distraer). Los aprendices y la memoria son herramientas de línea de comandos, no hooks: el brazo decide si las usa.
- El árbitro (Fable, esta sesión) no participa como brazo y no ayuda a ninguno; la aceptación es la letra del §5, no una prueba oculta.
- El repo de JUACO se lee, no se ejecuta con Pool: las puertas se juzgan por diseño y humo, no por serie.
