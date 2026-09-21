# ESTADO — una página, se reescribe en cada cierre (skill `/juaco-cierre`)

> Última reescritura: **21-sep-2026, 13:45** (coordinador). Si esta fecha tiene más de un día de atraso, el estado real está en la cola de
> `REGISTRO_etapas_1_2.md` y en la última sección de `HANDOFF.md`; corregir esta página antes de tocar nada.
> Historia completa: `REGISTRO_etapas_1_2.md` (sólo añadir). Narrativa: `HANDOFF.md`. Orden vigente: `PLAN.md`. Reglas: `EQUIPO.md` y `CLAUDE.md`.

## Tronco
**v14.2** (tag `v14.2-tronco`, 18-sep 21:25) = v14.1 + B-5 (división por conflicto disparada por R = 0 bajo retina distinta; repara el alias de
código). 20 archivos congelados (`python manifiesto.py` desde la raíz los verifica). Regla 1 en `CLAUDE.md`. Criterio para candidatos nuevos:
`CRITERIO_TRONCO_v2.md` (sobrevivir + generalizar + desdecirse + sin alias + no regresión conductual + coste + capacidad nueva declarada).

## Niveles del brief (porcentaje = lo declarado con réplica)
| nivel | estado | última evidencia |
|---|---|---|
| 1–4 (asociación, desaprender, generalizar, capacidad) | cerrados; nivel 4 con el negativo del alias reparado por B-5 (v14.2) | 18-sep |
| 5 (comunicación / transmisión) | **75 %**: N1 cerrado; referencia de FAMILIA exacta (k = 3) o de VARIANTE (sufijo), no ambas con la misma tabla; junta del 19-sep no cerró (C refutado ×2, B cae ×2, A pasa R1–R5 en una serie sin réplica, PAR 13 < 15) | 19-sep |
| 6 (mapa, dos metas y rodeo) | replicado: elige entre dos comidas recordadas y rodea el veneno recordado; no planifica; canje del mapa estructural, v14 sin mapa | 17-sep |
| 7 (composición, XOR) | 3T-k compone hasta 3; XOR CERRADA: prior estructural de pares (8 ejemplos, 1.000 ×2); hija dispersa en el tronco | 18-sep |
| 8 (aprendizaje abierto) | 40 %: curiosidad por progreso refutada; mundo vivo con dos necesidades es el primer mundo con más de una dimensión de valor | 18-sep |
| 9 (autonomía / modelo de sí mismo) | 30 %: allostasis mínima medida; r = descendientes − muertes ordena como la supervivencia; H-1: la muerte real no sostiene linajes | 18-sep |
| 10–13 (alma, familias, vivo) | exploratorio: serie ALMA (el alma razonada no gana al azar; el nodo transmite contenido); mundo de familias construido | 18-sep |

## Pendiente con paquete verificado (correr en este orden, un Pool a la vez)
1. **v15f bajo el criterio v2** — `python experimentos/creacion_A/corre_v15f_v2.py` (arnés 33/33; esqueleto de 9 etapas corre entero y da INCOMPLETO
   sin puertas medidas, `datos/v15f_v2_20260918_205648`). Decisión del director del 18-sep: sí.
2. **dE5** (sorpresa del mundo en la boca a dosis 5) — después de v15f. Decisión del director: sí.
3. **Fase 5, candidato B+A** (lectura conjuntiva de B + dos ganadoras de tipo distinto de A) — en diseño por `juaco-creador` desde el 21-sep
   en `experimentos/junta_fase5/BA/`. Nadie lo había probado junto.
4. **Fase 9**: cuerpo nuevo que aprende en menos de una vida (nodo leído por relevancia; conexión desde el nacimiento; reproducción desacoplada
   de la saciedad). Sin preregistro todavía.

## Errores
Último: **ERR-87** (21-sep: `lee_json` por `startswith` en los runners v13D/v13E; ningún veredicto cambia). Siguiente libre: **ERR-88**.
Reglas de equipo 1–14 en `EQUIPO.md`; regla derivada de ERR-87: "último JSON de un prefijo" siempre con prefijo + sello exacto.

## Datos
`datos/` plano (562 archivos, 84 MB). `datos/humo_no_registrado/` guarda humos y corridas sin dueño en el registro (no entran a git).
Desde el 21-sep los runners nuevos escriben sus humos en `datos/humo/`. Índice de carpetas de experimentos: `experimentos/INDICE.md`.

## Equipo y herramientas (21-sep-2026)
Agentes fijos (en `~/.claude/agents`, valen desde cualquier carpeta): `juaco-creador` (Opus), `juaco-compilador` (Opus), `juaco-auditor` (Sonnet,
solo lectura), `juaco-cronista` (Sonnet), `probador-haiku`, `explorador-haiku`. Skills: `/juaco-estado`, `/juaco-bloque`, `/juaco-cierre`,
`/juaco-err`, `/veredicto`, `/encargo`. Ninguno corre Pool, commitea ni mata procesos: sólo el coordinador. Coordinación de CPU: mirar los
procesos python vivos con su cmdline antes de lanzar (ERR-85, ERR-86).

## Decisiones que le tocan al director
1. Orden de corrida entre v15f-v2 y el candidato B+A cuando el paquete BA esté verificado (recomendado: v15f-v2 primero).
2. Si la fase 9 se abre ahora con un creador o espera a que la fase 5 cierre.
