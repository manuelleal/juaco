# PENDIENTE al cierre por tokens (25-sep-2026 ~17:05). Leer esto primero para retomar.

## Corriendo en el PC al cierre (no se mataron: terminan solos y escriben sus JSON)
1. **MURO, serie 1: GLOTU** (37001–37020, Pool 6; log `muro/serie_pool6.log`). Preregistro commiteado; auditor LISTO. El creador predice NO (0.75).
   Leer: `tail -40 experimentos/organelos/muro/serie_pool6.log`. Réplica (37021–37040) sólo si la serie no da NO.
2. **Puenteo** (Fable 1, `comite2/puenteo/`, EXPLORATORIO). Con 4 semillas: patas de O1 0.949 (4/4), boca_buena 0.907 (4/4),
   limpieza 0.21 y memoria 0.14 hunden. Leer con `python lee_puenteo.py` dentro de la carpeta.
3. **Fuera del molde** (Fable 2, `comite2/molde/`, EXPLORATORIO): pizarra, imita, espera. Leer su `HALLAZGOS.md` si existe.

## Listo para correr (sin correr)
- **MURO, segundo intento: GLOTU+PATAS**, PREREGISTRO_muro2.md (arnés 66/66, humo2 OK; el creador predice NO 0.72). Cuando termine la serie 1:
  `python experimentos/organelos/muro/corre_muro2.py --serie --desde 37101 --n 20 --pool 6`

## Lectura clave de la tarde
- La brecha de la carrera está en las DECISIONES DE ACCIÓN (a dónde ir, no comer lo bueno de sobra), no en la memoria ni en la limpieza.
- Las piezas de O1 cierran la brecha (+0.25..+0.31). Nuestras traducciones genéricas todavía no (+0.02).
- En esta pista, morder lo malo repone el mundo: quitarle al fundador esa mordida baja el establecimiento.
- Hito del día, ya en main: **F1 ARRANQUE EN FRÍO FUNCIONA ×2** (ECO).
