# Bitácora de la nube — noche del 23→24-sep-2026

> Sesión en la nube (Claude Code, `session_01RQB2Z9Hj9yA4LEoLeUWGcA`), rama **`nube/noche-20260924`**. Encargo: `NUBE.md` §2b.
> Horas en **UTC** (Bogotá = UTC − 5). Esta bitácora reemplaza, para la nube, a `ESTADO.md`, `REGISTRO_etapas_1_2.md` y `HANDOFF.md`,
> que no se tocan porque el PC los está usando. Mañana el coordinador integra.
> Los candidatos a ERR llevan numeración provisional **nube-N**, para no chocar con los ERR que el PC numere esta noche (último conocido:
> ERR-121).

## 0. Arranque (01:39)
- `git pull` de main: `81dea3e`. La rama `nube/noche-20260924` sale de `origin/main`.
- `python --version` da **3.11.15**: la línea del PATH no está en `~/.bashrc`. O el Setup script no la corrió, o todavía no está puesto.
  El contenedor se reinició a las 01:37, pero `/root/venv-juaco` sigue ahí. Todo se corre con `/root/venv-juaco/bin/python`: 3.13.12,
  numpy 2.4.3, numba 0.67.0 y scipy 1.17.1.
- `manifiesto.py --check`: los 20 congelados están intactos.
- Pool = 3 para las series. El cuarto núcleo queda para arneses y para lo exploratorio, con un proceso a la vez.

## 1. Series (veredicto por la letra del preregistro)

### 1a. `subida_n10b` — la familia pasa su tabla en vida
- **01:41 — arnés** `identidad_familia_b.py` (070e6524f79e3cc4): **42/42** en 75 s (PC: 126 s). Salida idéntica a la del PC; el diff
  normaliza sólo CRLF, fechas y tiempos.
- **01:42 — serie 12701–12720**, lanzada con este comando:
  `/root/venv-juaco/bin/python experimentos/subida_n10b/corre_n10b.py --serie --desde 12701 --n 20 --pool 3`
  - `corre_n10b.py` b7808bbb83fb038e · `PREREGISTRO_n10b.md` 100f83f74446a973.
  - Log: `experimentos/subida_n10b/datos/n10b_serie_s12701-12720_T100000_20260924_014236.log`.
  - Estado: **en curso**.

### 1b. JUACO-ECO (frente 2)
- **01:43 — arnés** `identidad_eco.py` (b70ec2f05915dc2e): **41/41** en 118 s (PC: 208 s). Salida idéntica a la del PC. Corrió en el
  núcleo libre mientras n10b usa los otros 3.
- **Observación, candidato a ERR nube-1 (menor, no bloquea):** el sha del runner en el preregistro no está al día.
  - El §0 de `PREREGISTRO_eco.md` cita `corre_eco.py` 0627f237b597523a.
  - El runner en main es 47d9cee4d6462116 (commit `bdb0aab`, 23-sep 19:51). Es el mismo que usó el humo `eco_humo_s19001_20260923_194831`,
    el que ejercita el juez actual (ERR-120).
  - La diferencia es la enmienda ERR-121 (P3c pasa a decidir), escrita antes de cualquier serie. El §0 no se actualizó.
  - La serie corre con el runner de main, y su log imprime el sha.

## 2. Exploratorio — **EXPLORATORIO, no es dato**
Carpeta: `experimentos/exploratorio_nube_20260924/` (su `NOTA_EXPLORATORIA.md` manda). Aquí va sólo el resumen.

_(pendiente)_

## 3. Decisiones del coordinador de la nube (hora, opción, alternativa descartada, porqué)
- **01:43 — el arnés de ECO corre ahora, en el núcleo libre, y no justo antes de su serie.**
  - Alternativa descartada: esperar a que termine n10b.
  - Por qué: ningún archivo de ECO se toca esta noche, y así un fallo aparece con horas de margen. Antes de lanzar la serie de ECO se
    vuelve a verificar el sha del runner.
- **01:45 — los candidatos a ERR se numeran como nube-N.** Así no chocan con el PC, que también numera esta noche.

## 4. Qué falló y qué propongo para mañana
_(al cierre)_
