# SELECCIÓN — réplica de la siembra (13-oct-2026)

Manda `../../PREREGISTRO.md`, sección "Réplica" (la decisión sobre falsas alarmas cruzó el umbral por una sola copia).

- **Bloques:** los mismos 10 de `../../siembra/SELECCION.md`, con los mismos archivos por copia (preregistro, `corre_*.py`,
  instrumentos que importa, JSON y `.log` en `datos/`, `VEREDICTO.md` copiado del REGISTRO; en `criterio_v4`, también la
  letra `CRITERIO_TRONCO_v4.md`).
- **Copias:** 20, dos por bloque, nombradas `r01`…`r20` en orden barajado con `random.Random(20261014)`.
- **Defectos:** nuevos; ninguno repite los de la primera siembra. Un defecto como máximo por copia.
- **Clave:** fuera del repositorio. Aquí sólo su sha256 (`CLAVE.sha256`), sellado antes de auditar.
- Los sha16 que citan los logs, JSON y veredictos de cada copia se resellaron sobre los archivos de esa copia, como en la
  primera siembra. Fechas de modificación uniformes.
